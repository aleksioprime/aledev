import asyncio
import logging
import time
from datetime import datetime, timezone
from email.message import EmailMessage
from email.utils import formataddr, formatdate, make_msgid
from uuid import UUID

import httpx
from jinja2 import Environment, FileSystemLoader, select_autoescape

from src.constants.base import (
    EmailStatus,
    FeedbackKind,
    FEEDBACK_SERVICES,
    FEEDBACK_BUDGETS,
)
from src.exceptions.base import NotFoundException
from src.models.feedback import Feedback
from src.repositories.uow import UnitOfWork
from src.schemas.feedback import (
    FeedbackCreateSchema,
    FeedbackQueryParams,
    FeedbackSchema,
    FeedbackStatsSchema,
    FeedbackUpdateSchema,
)
from src.schemas.pagination import PaginatedResponse
from src.services.mailer import Mailer, MailError

logger = logging.getLogger(__name__)

class FeedbackService:
    def __init__(self, settings, protection_settings, uow_factory=UnitOfWork):
        self.settings = settings
        self.protection_settings = protection_settings
        self.uow_factory = uow_factory
        self.mailer = Mailer(settings)

        self.jinja_env = Environment(
            loader=FileSystemLoader(self.settings.templates_path),
            autoescape=select_autoescape(["html", "xml"])
        )

    async def verify_feedback_request(
        self,
        captcha_token: str,
        honeypot: str,
        form_started_at: int,
        remote_ip: str | None = None,
    ) -> bool:
        if honeypot and honeypot.strip():
            logger.warning("[FeedbackService] Honeypot triggered")
            return False

        elapsed_ms = int(time.time() * 1000) - form_started_at
        min_elapsed_ms = self.protection_settings.min_form_fill_seconds * 1000
        if elapsed_ms < min_elapsed_ms:
            logger.warning(
                "[FeedbackService] Form submitted too fast: %sms < %sms",
                elapsed_ms,
                min_elapsed_ms,
            )
            return False

        if not self.protection_settings.turnstile_secret_key:
            logger.error("[FeedbackService] TURNSTILE_SECRET_KEY не задан")
            return False

        payload = {
            "secret": self.protection_settings.turnstile_secret_key,
            "response": captcha_token,
        }
        if remote_ip:
            payload["remoteip"] = remote_ip

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(
                    self.protection_settings.turnstile_verify_url,
                    data=payload,
                )
                response.raise_for_status()
                data = response.json()
        except Exception as e:
            logger.error(
                "[FeedbackService] Ошибка проверки Turnstile: %s",
                e,
                exc_info=True,
            )
            return False

        if not data.get("success", False):
            logger.warning(
                "[FeedbackService] Turnstile verification failed: %s",
                data.get("error-codes"),
            )
            return False

        return True

    # ------------------------------------------------------------------
    #  Сохранение обращения
    # ------------------------------------------------------------------

    async def create(self, body: FeedbackCreateSchema, ip: str | None, user_agent: str | None) -> UUID:
        """ Сохраняет обращение в БД; письмо отправляется отдельной задачей """
        uow = self.uow_factory()
        async with uow:
            feedback = await uow.feedback.create(
                kind=body.kind,
                name=body.name,
                email=str(body.email),
                contact=body.contact,
                service=body.service,
                budget=body.budget,
                deadline=body.deadline,
                message=body.message,
                lang=body.lang,
                email_status=EmailStatus.pending,
                ip=ip,
                user_agent=(user_agent or "")[:512] or None,
            )
            feedback_id = feedback.id
        logger.info("[FeedbackService] Сохранено обращение %s (%s) от %s", feedback_id, body.kind.value, body.email)
        return feedback_id

    # ------------------------------------------------------------------
    #  Отправка уведомления на почту (фоновая задача + воркер повторов)
    # ------------------------------------------------------------------

    async def notify(self, feedback_id: UUID) -> bool:
        """ Отправляет письмо по обращению. Возвращает True при успехе. """
        uow = self.uow_factory()
        async with uow:
            feedback = await uow.feedback.claim_for_email(feedback_id)
            if feedback is None:
                return False  # уже отправлено или отправляется другим процессом
            data = self._email_context(feedback)

        text, html = self._render(data)
        msg = self._build_message(data, text, html)

        values: dict
        try:
            result = await self.mailer.send(msg, text, html)
            values = {
                "email_status": EmailStatus.sent,
                "email_provider": result.provider,
                "email_error": "; ".join(result.errors) or None,
                "emailed_at": datetime.now(timezone.utc),
            }
            logger.info("[FeedbackService] Письмо по %s отправлено через %s", feedback_id, result.provider)
        except MailError as e:
            values = {"email_status": EmailStatus.failed, "email_error": str(e)[:2000]}
            logger.error("[FeedbackService] Письмо по %s не отправлено: %s", feedback_id, e)
        except Exception as e:  # noqa: BLE001
            values = {"email_status": EmailStatus.failed, "email_error": f"{type(e).__name__}: {e}"[:2000]}
            logger.error("[FeedbackService] Ошибка при отправке письма по %s", feedback_id, exc_info=True)

        uow = self.uow_factory()
        async with uow:
            await uow.feedback.update(feedback_id, **values)
        return values["email_status"] == EmailStatus.sent

    async def process_queue(self) -> int:
        """ Один проход воркера: досылает неотправленные письма """
        uow = self.uow_factory()
        async with uow:
            ids = await uow.feedback.get_retry_ids(self.settings.email_max_attempts)
            for feedback_id in ids:
                await uow.feedback.release_stuck(feedback_id)
        sent = 0
        for feedback_id in ids:
            if await self.notify(feedback_id):
                sent += 1
        return sent

    async def run_worker(self, stop: asyncio.Event) -> None:
        """ Фоновый цикл, запускается в lifespan приложения """
        interval = max(10, self.settings.email_retry_interval)
        logger.info("[FeedbackService] Воркер писем запущен (каждые %s с)", interval)
        while not stop.is_set():
            try:
                await self.process_queue()
            except Exception:  # noqa: BLE001 — воркер не должен падать
                logger.error("[FeedbackService] Ошибка воркера писем", exc_info=True)
            try:
                await asyncio.wait_for(stop.wait(), timeout=interval)
            except asyncio.TimeoutError:
                pass

    # ------------------------------------------------------------------
    #  Админка
    # ------------------------------------------------------------------

    async def get_all(self, params: FeedbackQueryParams) -> PaginatedResponse[FeedbackSchema]:
        uow = self.uow_factory()
        async with uow:
            items, total = await uow.feedback.get_all(params)
        return PaginatedResponse[FeedbackSchema](
            items=[FeedbackSchema.model_validate(i) for i in items],
            total=total,
            limit=params.limit,
            offset=params.offset,
            has_next=params.offset + params.limit < total,
            has_previous=params.offset > 0,
        )

    async def stats(self) -> FeedbackStatsSchema:
        uow = self.uow_factory()
        async with uow:
            return FeedbackStatsSchema(**await uow.feedback.stats())

    async def update(self, feedback_id: UUID, body: FeedbackUpdateSchema) -> FeedbackSchema:
        uow = self.uow_factory()
        async with uow:
            feedback = await uow.feedback.update(feedback_id, **body.model_dump(exclude_unset=True))
            if not feedback:
                raise NotFoundException("Обращение не найдено")
            return FeedbackSchema.model_validate(feedback)

    async def delete(self, feedback_id: UUID) -> None:
        uow = self.uow_factory()
        async with uow:
            if not await uow.feedback.delete(feedback_id):
                raise NotFoundException("Обращение не найдено")

    async def requeue(self, feedback_id: UUID) -> FeedbackSchema:
        """ Повторная отправка письма вручную из админки """
        uow = self.uow_factory()
        async with uow:
            feedback = await uow.feedback.update(
                feedback_id, email_status=EmailStatus.pending, email_attempts=0, email_error=None
            )
            if not feedback:
                raise NotFoundException("Обращение не найдено")
        await self.notify(feedback_id)
        uow = self.uow_factory()
        async with uow:
            return FeedbackSchema.model_validate(await uow.feedback.get_by_id(feedback_id))

    # ------------------------------------------------------------------
    #  Письмо
    # ------------------------------------------------------------------

    def _email_context(self, feedback: Feedback) -> dict:
        is_order = feedback.kind == FeedbackKind.order
        return {
            "id": str(feedback.id),
            "is_order": is_order,
            "kind_label": "Заказ" if is_order else "Вопрос",
            "name": feedback.name,
            "email": feedback.email,
            "contact": feedback.contact,
            "service": FEEDBACK_SERVICES.get(feedback.service) if feedback.service else None,
            "budget": FEEDBACK_BUDGETS.get(feedback.budget) if feedback.budget else None,
            "deadline": feedback.deadline,
            "message": feedback.message,
            "lang": feedback.lang,
            "created_at": feedback.created_at.astimezone().strftime("%d.%m.%Y %H:%M"),
        }

    def _render(self, data: dict) -> tuple[str, str]:
        lines = [f"Тип: {data['kind_label']}", f"Имя: {data['name']}", f"Email: {data['email']}"]
        if data["contact"]:
            lines.append(f"Контакт: {data['contact']}")
        if data["service"]:
            lines.append(f"Что нужно: {data['service']}")
        if data["budget"]:
            lines.append(f"Бюджет: {data['budget']}")
        if data["deadline"]:
            lines.append(f"Сроки: {data['deadline']}")
        text = "\n".join(lines) + f"\n\nСообщение:\n{data['message']}\n\nID: {data['id']}"
        html = self.jinja_env.get_template("feedback_email.html").render(**data)
        return text, html

    def _build_message(self, data: dict, text: str, html: str) -> EmailMessage:
        safe_name = " ".join(data["name"].split())  # защита от переносов строк в заголовке
        prefix = "🟢 Заказ" if data["is_order"] else "💬 Вопрос"

        msg = EmailMessage()
        msg["Subject"] = f"{prefix} с aledev.ru — {safe_name}"
        msg["From"] = formataddr((self.settings.feedback_sender_name, self.settings.sender))
        msg["To"] = self.settings.receiver
        msg["Reply-To"] = data["email"]
        msg["Date"] = formatdate(localtime=True)
        msg["Message-ID"] = make_msgid(domain=self.settings.sender.split("@")[-1] or None)
        msg.set_content(text)
        msg.add_alternative(html, subtype="html")
        return msg
