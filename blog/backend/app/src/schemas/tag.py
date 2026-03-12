"""
Схемы для тегов
"""

from typing import Optional
from pydantic import BaseModel, Field

from src.schemas.pagination import BasePaginationParams


class TagCreateSchema(BaseModel):
    """
    Схема для создания тега
    """
    name: str = Field(..., min_length=2, max_length=64, description="Название тега")

    class Config:
        from_attributes = True


class TagUpdateSchema(BaseModel):
    """
    Схема для обновления тега
    """
    name: Optional[str] = Field(None, min_length=2, max_length=64, description="Название тега")

    class Config:
        from_attributes = True


class TagQueryParams(BasePaginationParams):
    """
    Параметры фильтрации тегов
    """
    search: Optional[str] = Field(None, description="Поиск по названию тега")

    class Config:
        arbitrary_types_allowed = True