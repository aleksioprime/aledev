from typing import List
from uuid import UUID
from pydantic import BaseModel, Field

from src.constants.base import LangEnum
from src.schemas.pagination import BasePaginationParams


class ProjectQueryParams(BasePaginationParams):
    is_favorite: bool | None = Field(None, description="Метка изобранного проекта")

    class Config:
        arbitrary_types_allowed = True


class ProjectTranslationSchema(BaseModel):
    """
    Схема переводов данных проекта
    """
    lang: LangEnum = Field(..., description="Язык перевода, например 'ru' или 'en'")
    title: str = Field(..., description="Название проекта на данном языке")
    description: str | None = Field(None, description="Описание проекта на данном языке")

    class Config:
        from_attributes = True


class ProjectBaseSchema(BaseModel):
    """
    Базовая схема для представления данных проекта
    """
    id: UUID = Field(..., description="Уникальный идентификатор проекта")
    stack: str | None = Field(None, description="Используемый стек технологий")
    link: str | None = Field(None, description="Ссылка на проект")
    github_url: str | None = Field(None, description="Ссылка на репозиторий GitHub")
    demo_url: str | None = Field(None, description="Ссылка на демо-версию проекта")
    is_favorite: bool = Field(False, description="Является ли проект избранным")

    class Config:
        from_attributes = True



class ProjectSchema(ProjectBaseSchema):
    """
    Схема для представления данных проекта с переводами
    """
    translations: List[ProjectTranslationSchema] = Field(
        default_factory=list,
        description="Список переводов проекта на разные языки"
    )

    class Config:
        from_attributes = True


class ProjectWithTranslationSchema(ProjectBaseSchema):
    """
    Схема для представления данных проекта с одним переводом
    """
    translation: ProjectTranslationSchema = Field(..., description="Перевод проекта на выбранном языке")

    class Config:
        from_attributes = True


class ProjectTranslationCreateSchema(BaseModel):
    """
    Схема для создания перевода данных проекта
    """
    lang: LangEnum = Field(..., description="Язык перевода, например 'ru' или 'en'")
    title: str = Field(..., description="Название проекта на данном языке")
    description: str | None = Field(None, description="Описание проекта на данном языке")


class ProjectTranslationUpdateSchema(BaseModel):
    """
    Схема для обновления перевода данных проекта
    """
    title: str | None = Field(None, description="Название проекта на данном языке")
    description: str | None = Field(None, description="Описание проекта на данном языке")


class ProjectCreateSchema(BaseModel):
    """
    Схема для создания проекта
    """
    stack: str | None = Field(None, description="Используемый стек технологий")
    link: str | None = Field(None, description="Ссылка на проект")
    github_url: str | None = Field(None, description="Ссылка на репозиторий GitHub")
    demo_url: str | None = Field(None, description="Ссылка на демо-версию проекта")
    is_favorite: bool = Field(False, description="Является ли проект избранным")

    translations: list[ProjectTranslationCreateSchema] = Field(
        default_factory=list,
        description="Список переводов проекта"
    )


class ProjectUpdateSchema(BaseModel):
    """
    Схема для обновления проекта
    """
    stack: str | None = Field(None, description="Используемый стек технологий")
    link: str | None = Field(None, description="Ссылка на проект")
    github_url: str | None = Field(None, description="Ссылка на репозиторий GitHub")
    demo_url: str | None = Field(None, description="Ссылка на демо-версию проекта")
    is_favorite: bool | None = Field(None, description="Является ли проект избранным")

    translations: list[ProjectTranslationCreateSchema] | None = Field(
        None,
        description="Список переводов проекта для обновления"
    )
