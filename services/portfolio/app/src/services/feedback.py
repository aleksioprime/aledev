import logging

import httpx
from jinja2 import Environment, FileSystemLoader, select_autoescape

logger = logging.getLogger(__name__)

class FeedbackService:
    def __init__(self, settings):
        self.settings = settings

        self.jinja_env = Environment(
            loader=FileSystemLoader(self.settings.templates_path),
            autoescape=select_autoescape(["html", "xml"])
        )

    async def send_feedback(self, name: str, email: str, message: str):
        try:
            if not self.settings.resend_api_key:
                logger.error("[FeedbackService] RESEND_API_KEY не задан")
                return
            if not self.settings.feedback_receiver:
                logger.error("[FeedbackService] FEEDBACK_RECEIVER не задан")
                return

            subject = f"Обратная связь от {name}"
            text = (
                f"Имя: {name}\n"
                f"Email: {email}\n\n"
                f"Сообщение:\n{message}"
            )

            template = self.jinja_env.get_template("feedback_email.html")
            html = template.render(name=name, email=email, message=message)

            payload = {
                "from": self.settings.feedback_sender,
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
