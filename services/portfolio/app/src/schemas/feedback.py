from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator

from src.constants.base import (
    FeedbackKind,
    FeedbackStatus,
    EmailStatus,
    FEEDBACK_SERVICES,
    FEEDBACK_TRAINING_FORMATS,
    FEEDBACK_BUDGETS,
)
from src.schemas.pagination import BasePaginationParams


def _clean(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    return value or None


class FeedbackCreateSchema(BaseModel):
    """ Публичная форма обратной связи """
    kind: FeedbackKind = FeedbackKind.question
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    contact: str | None = Field(None, max_length=255, description="Telegram / телефон")
    service: str | None = Field(None, max_length=30, description="Тип работ (заказ) или формат (обучение)")
    budget: str | None = Field(None, max_length=30, description="Бюджет (для заказа)")
    deadline: str | None = Field(None, max_length=100, description="Сроки (для заказа)")
    message: str = Field(..., min_length=10, max_length=4000)
    lang: Literal["ru", "en"] | None = None

    captcha_token: str = Field(..., min_length=10, max_length=4096)
    website: str = Field("", max_length=0)
    form_started_at: int = Field(..., gt=0)

    @field_validator("name", mode="before")
    @classmethod
    def normalize_name(cls, value):
        """
        Схлопывает пробелы и переносы в имени
        """
        # имя попадает в тему письма - схлопываем переносы и лишние пробелы
        return " ".join(value.split()) if isinstance(value, str) else value

    @field_validator("message", mode="before")
    @classmethod
    def strip_message(cls, value):
        """
        Обрезает пробелы в тексте сообщения
        """
        return value.strip() if isinstance(value, str) else value

    @field_validator("contact", "deadline", "service", "budget", mode="before")
    @classmethod
    def strip_optional(cls, value):
        """
        Превращает пустые строки в None
        """
        return _clean(value) if isinstance(value, str) or value is None else value

    @field_validator("budget")
    @classmethod
    def check_budget(cls, value):
        """
        Проверяет бюджет по справочнику
        """
        if value is not None and value not in FEEDBACK_BUDGETS:
            raise ValueError("Недопустимый бюджет")
        return value

    @model_validator(mode="after")
    def check_kind_fields(self):
        """
        Проверяет поля, зависящие от типа обращения
        """
        if self.kind == FeedbackKind.question:
            # у вопроса нет полей заказа
            self.service = self.budget = self.deadline = None
            return self
        # у заказа - тип работ, у обучения - формат занятий
        allowed = FEEDBACK_SERVICES if self.kind == FeedbackKind.order else FEEDBACK_TRAINING_FORMATS
        if self.service is not None and self.service not in allowed:
            raise ValueError("Недопустимое значение service для этого типа обращения")
        return self


class FeedbackSchema(BaseModel):
    """ Обращение для админки """
    id: UUID
    kind: FeedbackKind
    name: str
    email: str
    contact: str | None = None
    service: str | None = None
    budget: str | None = None
    deadline: str | None = None
    message: str
    lang: str | None = None
    status: FeedbackStatus
    admin_note: str | None = None
    email_status: EmailStatus
    email_attempts: int
    email_provider: str | None = None
    email_error: str | None = None
    emailed_at: datetime | None = None
    ip: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class FeedbackUpdateSchema(BaseModel):
    """
    Изменение статуса и заметки обращения
    """
    status: FeedbackStatus | None = None
    admin_note: str | None = Field(None, max_length=4000)


class FeedbackQueryParams(BasePaginationParams):
    """
    Параметры фильтрации и пагинации обращений
    """
    kind: FeedbackKind | None = None
    status: FeedbackStatus | None = None
    email_status: EmailStatus | None = None
    search: str | None = None

    class Config:
        arbitrary_types_allowed = True


class FeedbackStatsSchema(BaseModel):
    """
    Счётчики обращений
    """
    total: int
    new: int
    orders: int
    trainings: int
    questions: int
    email_failed: int
