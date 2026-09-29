from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field

from src.constants.base import LangEnum


class MentoringPageTranslationSchema(BaseModel):
    """
    Перевод текста секции наставничества
    """
    lang: LangEnum
    kicker: str
    title_start: str
    title_accent: str
    lead: str

    class Config:
        from_attributes = True


class MentoringMetricTranslationSchema(BaseModel):
    """
    Перевод подписи к цифре
    """
    lang: LangEnum
    label: str

    class Config:
        from_attributes = True


class MentoringMetricSchema(BaseModel):
    """
    Цифра секции наставничества
    """
    id: UUID
    key: str
    value: str
    order: int
    translations: List[MentoringMetricTranslationSchema] = Field(default_factory=list)

    class Config:
        from_attributes = True


class MentoringPageSchema(BaseModel):
    """
    Контент секции наставничества
    """
    id: UUID
    slug: str
    is_published: bool
    created_at: datetime
    updated_at: datetime
    translations: List[MentoringPageTranslationSchema] = Field(default_factory=list)
    metrics: List[MentoringMetricSchema] = Field(default_factory=list)

    class Config:
        from_attributes = True


class MentoringPageTranslationUpdateSchema(BaseModel):
    """
    Перевод текста секции при обновлении
    """
    lang: LangEnum
    kicker: str = Field(..., min_length=1, max_length=255)
    title_start: str = Field(..., min_length=1, max_length=255)
    title_accent: str = Field(..., min_length=1, max_length=255)
    lead: str = Field(..., min_length=1)


class MentoringMetricTranslationUpdateSchema(BaseModel):
    """
    Перевод подписи к цифре при обновлении
    """
    lang: LangEnum
    label: str = Field(..., min_length=1, max_length=255)


class MentoringMetricUpdateSchema(BaseModel):
    """
    Цифра секции при обновлении
    """
    key: str = Field(..., min_length=1, max_length=40)
    value: str = Field(..., min_length=1, max_length=40)
    order: int = Field(0, ge=0)
    translations: List[MentoringMetricTranslationUpdateSchema] = Field(default_factory=list)


class MentoringPageUpdateSchema(BaseModel):
    """
    Данные для обновления секции наставничества
    """
    is_published: bool = True
    translations: List[MentoringPageTranslationUpdateSchema] = Field(..., min_length=1)
    metrics: List[MentoringMetricUpdateSchema] = Field(default_factory=list)
