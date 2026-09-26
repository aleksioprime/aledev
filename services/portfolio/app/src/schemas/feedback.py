from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator

from src.constants.base import (
    FeedbackKind,
    FeedbackStatus,
    EmailStatus,
    FEEDBACK_SERVICES,
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
    service: str | None = Field(None, max_length=30, description="Тип работ (для заказа)")
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
        # имя попадает в тему письма — схлопываем переносы и лишние пробелы
        return " ".join(value.split()) if isinstance(value, str) else value

    @field_validator("message", mode="before")
    @classmethod
    def strip_message(cls, value):
        return value.strip() if isinstance(value, str) else value

    @field_validator("contact", "deadline", "service", "budget", mode="before")
    @classmethod
    def strip_optional(cls, value):
        return _clean(value) if isinstance(value, str) or value is None else value

    @field_validator("service")
    @classmethod
    def check_service(cls, value):
        if value is not None and value not in FEEDBACK_SERVICES:
            raise ValueError("Недопустимый тип работ")
        return value

    @field_validator("budget")
    @classmethod
    def check_budget(cls, value):
        if value is not None and value not in FEEDBACK_BUDGETS:
            raise ValueError("Недопустимый бюджет")
        return value

    @model_validator(mode="after")
    def drop_order_fields_for_question(self):
        # Поля заказа имеют смысл только для заказа
        if self.kind == FeedbackKind.question:
            self.service = self.budget = self.deadline = None
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
    status: FeedbackStatus | None = None
    admin_note: str | None = Field(None, max_length=4000)


class FeedbackQueryParams(BasePaginationParams):
    kind: FeedbackKind | None = None
    status: FeedbackStatus | None = None
    search: str | None = None

    class Config:
        arbitrary_types_allowed = True


class FeedbackStatsSchema(BaseModel):
    total: int
    new: int
    orders: int
    questions: int
    email_failed: int
