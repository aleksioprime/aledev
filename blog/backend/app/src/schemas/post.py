from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime

from src.schemas.pagination import BasePaginationParams


class PostOrderSchema(BaseModel):
    id: UUID = Field(..., description="Уникальный идентификатор проекта")
    order: int = Field(0, ge=0, description="Порядок")


class PostQueryParams(BasePaginationParams):
    is_favorite: bool | None = Field(None, description="Метка изобранного проекта")

    class Config:
        arbitrary_types_allowed = True


class TagSchema(BaseModel):
    id: int = Field(..., description="Идентификатор тега (int)")
    name: str = Field(..., description="Название тега (человекочитаемое)")
    slug: str = Field(..., description="Слаг тега (для URL/фильтрации)")

    class Config:
        from_attributes = True


class CategorySchema(BaseModel):
    id: UUID = Field(..., description="UUID категории")
    name: str = Field(..., description="Название категории")
    slug: str = Field(..., description="Слаг категории")

    class Config:
        from_attributes = True


class PostBaseSchema(BaseModel):
    """
    Базовая схема поста (без содержимого статьи)
    """
    id: UUID = Field(..., description="UUID поста")
    order: int = Field(0, ge=0, description="Порядок")
    title: str = Field(..., description="Заголовок поста")
    slug: str = Field(..., description="Слаг поста (для URL)")
    excerpt: Optional[str] = Field(None, description="Краткое описание")
    url: Optional[str] = Field(None, description="URL обложки")
    published: bool = Field(True, description="Опубликован ли пост")
    published_at: Optional[datetime] = Field(None, description="Время публикации")
    created_at: datetime = Field(..., description="Дата создания")
    updated_at: datetime = Field(..., description="Дата изменения")
    category: Optional[CategorySchema] = Field(None, description="Категория поста")
    tags: List[TagSchema] = Field(default_factory=list, description="Список тегов")

    class Config:
        from_attributes = True



class PostSchema(PostBaseSchema):
    """
    Детальная схема поста (включает контент HTML)
    """
    content: str = Field(..., description="HTML содержимое статьи (CKEditor)")

    class Config:
        from_attributes = True


class PostCreateSchema(BaseModel):
    """
    Схема для создания поста
    - slug генерится на бэкенде
    - category_slug: слаг существующей категории
    - tags: список слагов/названий тегов
    """
    order: int = Field(0, ge=0, description="Порядок")
    title: str = Field(..., min_length=3, max_length=300, description="Заголовок поста")
    excerpt: Optional[str] = Field(None, max_length=500, description="Краткое описание")
    content: str = Field(..., description="HTML содержимое статьи (CKEditor)")
    url: Optional[str] = Field(None, description="URL обложки")
    published: bool = Field(True, description="Опубликован ли пост")
    published_at: Optional[datetime] = Field(None, description="Время публикации")
    category_slug: Optional[str] = Field(None, description="Слаг категории")
    tags: List[str] = Field(default_factory=list, description="Список тегов (slug или name)")


class PostUpdateSchema(BaseModel):
    """
    Схема для обновления поста
    """
    order: Optional[int] = Field(None, ge=0, description="Порядок")
    title: Optional[str] = Field(None, min_length=3, max_length=300, description="Заголовок поста")
    excerpt: Optional[str] = Field(None, max_length=500, description="Краткое описание")
    content: Optional[str] = Field(None, description="HTML содержимое статьи (CKEditor)")
    url: Optional[str] = Field(None, description="URL обложки")
    published: Optional[bool] = Field(None, description="Опубликован ли пост")
    published_at: Optional[datetime] = Field(None, description="Время публикации")
    category_slug: Optional[str] = Field(None, description="Слаг категории")
    tags: Optional[List[str]] = Field(None, description="Полная замена списка тегов (slug или name)")
