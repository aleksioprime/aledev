from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field

from src.constants.base import LangEnum
from src.schemas.pagination import BasePaginationParams


class AchievementQueryParams(BasePaginationParams):
    """
    Параметры фильтрации и пагинации достижений
    """
    category: str | None = Field(None, max_length=40)
    scope: str | None = Field(None, max_length=30)

    class Config:
        arbitrary_types_allowed = True


class AchievementTranslationSchema(BaseModel):
    """
    Перевод достижения
    """
    lang: LangEnum
    title: str
    organization: str | None = None
    result: str | None = None
    short_description: str | None = None
    description: str | None = None

    class Config:
        from_attributes = True


class AchievementSchema(BaseModel):
    """
    Достижение с переводами
    """
    id: UUID
    category: str
    scope: str
    year: int | None = None
    source_url: str | None = None
    image_url: str | None = None
    order: int
    is_featured: bool
    is_published: bool
    created_at: datetime
    updated_at: datetime
    translations: List[AchievementTranslationSchema] = Field(default_factory=list)

    class Config:
        from_attributes = True


class AchievementTranslationCreateSchema(BaseModel):
    """
    Перевод достижения при создании
    """
    lang: LangEnum
    title: str = Field(..., min_length=1, max_length=255)
    organization: str | None = Field(None, max_length=255)
    result: str | None = Field(None, max_length=255)
    short_description: str | None = Field(None, max_length=500)
    description: str | None = None


class AchievementCreateSchema(BaseModel):
    """
    Данные для создания достижения
    """
    category: str = Field(..., min_length=1, max_length=40)
    scope: str = Field(..., min_length=1, max_length=30)
    year: int | None = Field(None, ge=1900, le=2200)
    source_url: str | None = Field(None, max_length=500)
    image_url: str | None = Field(None, max_length=500)
    order: int = Field(0, ge=0)
    is_featured: bool = False
    is_published: bool = True
    translations: List[AchievementTranslationCreateSchema] = Field(default_factory=list)


class AchievementUpdateSchema(BaseModel):
    """
    Данные для обновления достижения
    """
    category: str | None = Field(None, min_length=1, max_length=40)
    scope: str | None = Field(None, min_length=1, max_length=30)
    year: int | None = Field(None, ge=1900, le=2200)
    source_url: str | None = Field(None, max_length=500)
    image_url: str | None = Field(None, max_length=500)
    order: int | None = Field(None, ge=0)
    is_featured: bool | None = None
    is_published: bool | None = None
    translations: List[AchievementTranslationCreateSchema] | None = None
