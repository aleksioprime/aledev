"""
Схемы для категорий
"""

from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

from src.schemas.pagination import BasePaginationParams


class CategoryCreateSchema(BaseModel):
    """
    Схема для создания категории
    """
    name: str = Field(..., min_length=3, max_length=80, description="Название категории")
    parent_id: Optional[UUID] = Field(None, description="ID родительской категории")

    class Config:
        from_attributes = True


class CategoryUpdateSchema(BaseModel):
    """
    Схема для обновления категории
    """
    name: Optional[str] = Field(None, min_length=3, max_length=80, description="Название категории")
    parent_id: Optional[UUID] = Field(None, description="ID родительской категории")

    class Config:
        from_attributes = True


class CategoryQueryParams(BasePaginationParams):
    """
    Параметры фильтрации категорий
    """
    parent_id: Optional[UUID] = Field(None, description="Фильтр по родительской категории")

    class Config:
        arbitrary_types_allowed = True