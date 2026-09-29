import asyncio
import logging
import smtplib
import ssl
from dataclasses import dataclass
from email.message import EmailMessage

import httpx

logger = logging.getLogger(__name__)


class MailError(Exception):
    """
    Письмо не удалось отправить ни одним способом
    """
    pass


@dataclass
class MailResult:
    """
    Результат отправки письма
    """
    provider: str
    errors: list[str]


class Mailer:
    """
    Отправка писем: основной канал - SMTP Яндекс Почты,
    запасной - Resend API (если задан RESEND_API_KEY).
    """

    def __init__(self, settings):
        self.settings = settings

    @property
    def smtp_configured(self) -> bool:
        """
        Заданы ли логин и пароль SMTP
        """
        return bool(self.settings.smtp_user and self.settings.smtp_password)

    @property
    def resend_configured(self) -> bool:
        """
        Задан ли ключ Resend
        """
        return bool(self.settings.resend_api_key)

    async def send(self, msg: EmailMessage, text: str, html: str) -> MailResult:
        """
        Отправляет письмо через SMTP, при ошибке через Resend
        """
        errors: list[str] = []

        if self.smtp_configured:
            try:
                await asyncio.to_thread(self._send_smtp, msg)
                return MailResult("yandex", errors)
            except smtplib.SMTPAuthenticationError as e:
                errors.append(f"SMTP auth: {e.smtp_code} {e.smtp_error!r} - проверьте пароль приложения Яндекса")
            except Exception as e:  # noqa: BLE001 - любая ошибка SMTP ведёт к запасному каналу
                errors.append(f"SMTP: {type(e).__name__}: {e}")
            logger.warning("[Mailer] SMTP не отправил письмо: %s", errors[-1])
        else:
            errors.append("SMTP не настроен (SMTP_USER / SMTP_PASSWORD)")

        if self.resend_configured:
            try:
                await self._send_resend(msg, text, html)
                return MailResult("resend", errors)
            except Exception as e:  # noqa: BLE001
                errors.append(f"Resend: {type(e).__name__}: {e}")
                logger.warning("[Mailer] Resend не отправил письмо: %s", errors[-1])

        raise MailError("; ".join(errors))

    def _send_smtp(self, msg: EmailMessage) -> None:
        s = self.settings
        context = ssl.create_default_context()
        if s.smtp_use_ssl:
            with smtplib.SMTP_SSL(s.smtp_host, s.smtp_port, timeout=s.smtp_timeout, context=context) as server:
                server.login(s.smtp_user, s.smtp_password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(s.smtp_host, s.smtp_port, timeout=s.smtp_timeout) as server:
                server.starttls(context=context)
                server.login(s.smtp_user, s.smtp_password)
                server.send_message(msg)

    async def _send_resend(self, msg: EmailMessage, text: str, html: str) -> None:
        s = self.settings
        payload = {
            "from": f"{s.feedback_sender_name} <{s.resend_sender}>",
            "to": [msg["To"]],
            "subject": msg["Subject"],
            "html": html,
            "text": text,
        }
        if msg["Reply-To"]:
            payload["reply_to"] = msg["Reply-To"]

        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(
                f"{s.resend_api_base_url}/emails",
                json=payload,
                headers={"Authorization": f"Bearer {s.resend_api_key}"},
            )
        if response.status_code >= 400:
            raise MailError(f"HTTP {response.status_code}: {response.text[:300]}")
