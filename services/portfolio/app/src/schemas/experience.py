from typing import List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

from src.constants.base import LangEnum
from src.schemas.pagination import BasePaginationParams


class ExperienceQueryParams(BasePaginationParams):

    class Config:
        arbitrary_types_allowed = True


class ExperienceTranslationSchema(BaseModel):
    """
    Схема перевода для опыта работы
    """
    lang: LangEnum = Field(..., description="Язык перевода, например 'ru' или 'en'")
    position: str = Field(..., description="Должность/позиция на данном языке")
    company: str = Field(..., description="Компания/организация на данном языке")
    description: str | None = Field(None, description="Описание опыта на данном языке")

    class Config:
        from_attributes = True


class ExperienceBaseSchema(BaseModel):
    """
    Базовая схема для представления записей об опыте работы
    """
    id: UUID = Field(..., description="Уникальный идентификатор опыта")
    start_date: datetime = Field(..., description="Дата начала")
    end_date: datetime | None = Field(None, description="Дата окончания (если есть)")
    is_current: bool = Field(False, description="Текущий опыт?")
    created_at: datetime = Field(..., description="Дата создания записи")

    class Config:
        from_attributes = True



class ExperienceSchema(ExperienceBaseSchema):
    """
    Схема для представления данных опыта работы с переводами
    """
    translations: List[ExperienceTranslationSchema] = Field(
        default_factory=list,
        description="Список переводов опыта на разные языки"
    )

    class Config:
        from_attributes = True


class ExperienceWithTranslationSchema(ExperienceBaseSchema):
    """
    Схема для представления данных опыта работы с одним переводом
    """
    translation: ExperienceTranslationSchema = Field(..., description="Перевод опыта на выбранном языке")

    class Config:
        from_attributes = True


class ExperienceTranslationCreateSchema(BaseModel):
    """
    Схема для создания перевода опыта работы
    """
    lang: LangEnum = Field(..., description="Язык перевода")
    position: str = Field(..., description="Должность/позиция")
    company: str = Field(..., description="Компания/организация")
    description: str | None = Field(None, description="Описание")


class ExperienceTranslationUpdateSchema(BaseModel):
    """
    Схема для обновления перевода опыта работы
    """
    position: str | None = Field(None, description="Должность/позиция")
    company: str | None = Field(None, description="Компания/организация")
    description: str | None = Field(None, description="Описание")


class ExperienceCreateSchema(BaseModel):
    """
    Схема для создания записи об опыте работы
    """
    start_date: datetime = Field(..., description="Дата начала")
    end_date: datetime | None = Field(None, description="Дата окончания")
    is_current: bool = Field(False, description="Текущий опыт?")

    translations: List[ExperienceTranslationCreateSchema] = Field(
        default_factory=list,
        description="Список переводов опыта"
    )


class ExperienceUpdateSchema(BaseModel):
    """
    Схема для обновления записи об опыте работы
    """
    start_date: datetime | None = Field(None, description="Дата начала")
    end_date: datetime | None = Field(None, description="Дата окончания")
    is_current: bool | None = Field(None, description="Текущий опыт?")
    translations: List[ExperienceTranslationUpdateSchema] | None = Field(
        None,
        description="Список переводов опыта для обновления"
    )
