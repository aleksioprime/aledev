import logging
import time

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

    async def send_feedback(self, name: str, email: str, message: str):
        try:
            if not self.settings.resend_api_key:
                logger.error("[FeedbackService] RESEND_API_KEY не задан")
                return
            if not self.settings.feedback_receiver:
                logger.error("[FeedbackService] FEEDBACK_RECEIVER не задан")
                return

            subject = f"Сообщение с aledev.ru"
            text = (
                f"Имя: {name}\n"
                f"Email: {email}\n\n"
                f"Сообщение:\n{message}"
            )

            template = self.jinja_env.get_template("feedback_email.html")
            html = template.render(name=name, email=email, message=message)

            payload = {
                "from": f"{self.settings.feedback_sender_name} <{self.settings.feedback_sender}>",
                "to": [self.settings.feedback_receiver],
                "subject": subject,
                "html": html,
                "text": text,
                "reply_to": email,
            }
            headers = {
                "Authorization": f"Bearer {self.settings.resend_api_key}",
                "Content-Type": "application/json",
            }

            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(
                    f"{self.settings.resend_api_base_url}/emails",
                    json=payload,
                    headers=headers,
                )
                response.raise_for_status()
                response_data = response.json()

            logger.info(
                "Feedback email sent via Resend from %s, id=%s",
                email,
                response_data.get("id"),
            )

        except httpx.HTTPStatusError as e:
            logger.error(
                "[FeedbackService] Resend вернул ошибку: status=%s body=%s",
                e.response.status_code,
                e.response.text,
                exc_info=True,
            )
        except Exception as e:
            logger.error(f"[FeedbackService] Ошибка при отправке письма: {e}", exc_info=True)
