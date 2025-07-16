import aiosmtplib
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader, select_autoescape


class FeedbackService:
    def __init__(self, settings):
        self.settings = settings

        self.jinja_env = Environment(
            loader=FileSystemLoader(self.settings.templates_path),
            autoescape=select_autoescape(["html", "xml"])
        )

    async def send_feedback(self, name: str, email: str, message: str):
        msg = EmailMessage()
        msg["Subject"] = f"Обратная связь от {name}"
        msg["From"] = self.settings.smtp_user
        msg["To"] = self.settings.feedback_receiver

        text = (
            f"Имя: {name}\n"
            f"Email: {email}\n\n"
            f"Сообщение:\n{message}"
        )
        msg.set_content(text)

        template = self.jinja_env.get_template("feedback_email.html")
        html = template.render(name=name, email=email, message=message)

        msg.add_alternative(html, subtype="html")

        await aiosmtplib.send(
            msg,
            hostname=self.settings.smtp_host,
            port=self.settings.smtp_port,
            username=self.settings.smtp_user,
            password=self.settings.smtp_password,
            use_tls=True,
        )
