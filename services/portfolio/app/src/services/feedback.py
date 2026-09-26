import asyncio
import logging
import smtplib
import ssl
import time
from email.message import EmailMessage
from email.utils import formataddr, formatdate, make_msgid

import httpx
from jinja2 import Environment, FileSystemLoader, select_autoescape

logger = logging.getLogger(__name__)

class FeedbackService:
    def __init__(self, settings, protection_settings):
        self.settings = settings
        self.protection_settings = protection_settings

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

    def _build_message(self, name: str, email: str, message: str) -> EmailMessage:
        text = (
            f"Имя: {name}\n"
            f"Email: {email}\n\n"
            f"Сообщение:\n{message}"
        )
        template = self.jinja_env.get_template("feedback_email.html")
        html = template.render(name=name, email=email, message=message)

        msg = EmailMessage()
        safe_name = " ".join(name.split())  # защита от переносов строк в заголовке
        msg["Subject"] = f"Сообщение с aledev.ru от {safe_name}"
        msg["From"] = formataddr((self.settings.feedback_sender_name, self.settings.sender))
        msg["To"] = self.settings.receiver
        msg["Reply-To"] = email
        msg["Date"] = formatdate(localtime=True)
        msg["Message-ID"] = make_msgid(domain=self.settings.sender.split("@")[-1] or None)
        msg.set_content(text)
        msg.add_alternative(html, subtype="html")
        return msg

    def _send_smtp(self, msg: EmailMessage) -> None:
        s = self.settings
        if s.smtp_use_ssl:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(s.smtp_host, s.smtp_port, timeout=s.smtp_timeout, context=context) as server:
                server.login(s.smtp_user, s.smtp_password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(s.smtp_host, s.smtp_port, timeout=s.smtp_timeout) as server:
                server.starttls(context=ssl.create_default_context())
                server.login(s.smtp_user, s.smtp_password)
                server.send_message(msg)

    async def send_feedback(self, name: str, email: str, message: str):
        try:
            if not self.settings.smtp_user or not self.settings.smtp_password:
                logger.error("[FeedbackService] SMTP_USER / SMTP_PASSWORD не заданы")
                return
            if not self.settings.receiver:
                logger.error("[FeedbackService] FEEDBACK_RECEIVER не задан")
                return

            msg = self._build_message(name, email, message)
            # smtplib блокирующий — выполняем в отдельном потоке
            await asyncio.to_thread(self._send_smtp, msg)

            logger.info("Feedback email sent via %s from %s", self.settings.smtp_host, email)

        except smtplib.SMTPAuthenticationError as e:
            logger.error(
                "[FeedbackService] Ошибка авторизации SMTP (проверьте пароль приложения Яндекса): %s",
                e,
                exc_info=True,
            )
        except Exception as e:
            logger.error(f"[FeedbackService] Ошибка при отправке письма: {e}", exc_info=True)
