import os
from typing import List
from datetime import timedelta

from pydantic import Field
from pydantic_settings import BaseSettings


class DBSettings(BaseSettings):
    """
    Конфигурация для настроек базы данных
    """

    name: str = Field(alias='DB_NAME', default='database')
    user: str = Field(alias='DB_USER', default='admin')
    password: str = Field(alias='DB_PASSWORD', default='123qwe')
    host: str = Field(alias='DB_HOST', default='127.0.0.1')
    port: int = Field(alias='DB_PORT', default=5432)
    show_query: bool = Field(alias='SHOW_SQL_QUERY', default=False)

    @property
    def _base_url(self) -> str:
        """ Формирует базовый URL для подключения к базе данных """
        return f"{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    @property
    def dsn(self) -> str:
        """ Формирует DSN строку для подключения к базе данных с использованием asyncpg """
        return f"postgresql+asyncpg://{self._base_url}"


class JWTSettings(BaseSettings):
    """
    Конфигурация для настроек JWT
    """

    secret_key: str = Field(
        alias='JWT_SECRET_KEY',
        default='7Fp0SZsBRKqo1K82pnQ2tcXV9XUfuiIJxpDcE5FofP2fL0vlZw3SOkI3YYLpIGP',
    )
    algorithm: str = Field(alias='JWT_ALGORITHM', default='HS256')
    access_token_expire_time: timedelta = Field(default=timedelta(minutes=15))
    refresh_token_expire_time: timedelta = Field(default=timedelta(days=10))


class MediaSettings(BaseSettings):
    base: str = "media"

    @property
    def base_path(self) -> str:
        return os.path.abspath(self.base)

    def __getattr__(self, name: str) -> str:
        if name.endswith("_path"):
            key = name[:-5]  # remove _path
            return os.path.join(self.base_path, key)
        if name.endswith("_url"):
            key = name[:-4]  # remove _url
            return f"/{self.base}/{key}"
        raise AttributeError(f"No such attribute: {name}")


class EmailSettings(BaseSettings):
    resend_api_key: str = Field(alias="RESEND_API_KEY", default="")
    resend_api_base_url: str = Field(alias="RESEND_API_BASE_URL", default="https://api.resend.com")
    feedback_sender: str = Field(alias="FEEDBACK_SENDER", default="no-reply@aledev.ru")
    feedback_receiver: str = Field(alias="FEEDBACK_RECEIVER", default="admin@yourdomain.com")
    templates_path: str = Field(
        alias="EMAIL_TEMPLATES_PATH",
        default=os.path.join(os.path.dirname(__file__), "../templates")
    )

class FeedbackProtectionSettings(BaseSettings):
    turnstile_secret_key: str = Field(alias="TURNSTILE_SECRET_KEY", default="")
    turnstile_verify_url: str = Field(
        alias="TURNSTILE_VERIFY_URL",
        default="https://challenges.cloudflare.com/turnstile/v0/siteverify",
    )
    min_form_fill_seconds: int = Field(alias="FEEDBACK_MIN_FORM_FILL_SECONDS", default=2)


class Settings(BaseSettings):
    project_name: str = Field(alias="PROJECT_NAME", default="AledevPortfolio")
    project_description: str = Field(
        alias="PROJECT_DESCRIPTION", default="Portfolio service for ALEDEV application"
    )

    jwt: JWTSettings = JWTSettings()
    db: DBSettings = DBSettings()
    media: MediaSettings = MediaSettings()
    email: EmailSettings = EmailSettings()
    feedback_protection: FeedbackProtectionSettings = FeedbackProtectionSettings()

    default_host: str = "0.0.0.0"
    default_port: int = 8000

    cors_allow_origins_str: str = Field(
        alias="CORS_ALLOW_ORIGINS",
        default="http://localhost,http://127.0.0.1,https://aledev.ru,https://www.aledev.ru",
    )
    cors_allow_origin_regex: str = Field(
        alias="CORS_ALLOW_ORIGIN_REGEX",
        default=r"^https?://([a-z0-9-]+\.)?aledev\.ru$",
    )

    @property
    def cors_allow_origins(self) -> List[str]:
        """Преобразует строку cors_allow_origins_str в список"""
        return [origin.strip() for origin in self.cors_allow_origins_str.split(",") if origin.strip()]


settings = Settings()
