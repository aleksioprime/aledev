"""
Репозиторий для работы с категориями
"""

from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.exc import NoResultFound

from src.models.post import Category
from src.repositories.base import BaseSQLRepository
from src.schemas.category import CategoryCreateSchema, CategoryUpdateSchema, CategoryQueryParams
from src.utils.slug import generate_slug, ensure_unique_slug


class BaseCategoryRepository(ABC):

    @abstractmethod
    async def get_by_id(self, category_id: UUID):
        ...

    @abstractmethod
    async def get_by_slug(self, slug: str):
        ...

    @abstractmethod
    async def get_all(self, params: CategoryQueryParams):
        ...

    @abstractmethod
    async def create(self, body: CategoryCreateSchema):
        ...

    @abstractmethod
    async def update(self, category_id: UUID, body: CategoryUpdateSchema):
        ...

    @abstractmethod
    async def delete(self, category_id: UUID):
        ...


class CategoryRepository(BaseCategoryRepository, BaseSQLRepository):

    async def get_by_id(self, category_id: UUID) -> Category | None:
        """
        Получает категорию по её ID
        """
        stmt = select(Category).where(Category.id == category_id)
        result = await self.session.execute(stmt)
        return result.scalars().unique().one_or_none()

    async def get_by_slug(self, slug: str) -> Category | None:
        """
        Получает категорию по её slug
        """
        stmt = select(Category).where(Category.slug == slug)
        result = await self.session.execute(stmt)
        return result.scalars().unique().one_or_none()

    async def get_all(self, params: CategoryQueryParams) -> tuple[list[Category], int]:
        """
        Получает пагинированный список категорий
        """
        stmt = select(Category)
        count_stmt = select(func.count()).select_from(Category)

        # Фильтр по родительской категории
        if params.parent_id is not None:
            stmt = stmt.where(Category.parent_id == params.parent_id)
            count_stmt = count_stmt.where(Category.parent_id == params.parent_id)

        stmt = stmt.order_by(Category.name).limit(params.limit).offset(params.offset)

        result = await self.session.execute(stmt)
        categories = result.scalars().unique().all()

        total = (await self.session.execute(count_stmt)).scalar_one()
        return categories, total

    async def create(self, body: CategoryCreateSchema) -> Category:
        """
        Создаёт новую категорию
        """
        # Генерируем slug из названия
        base_slug = generate_slug(body.name)
        unique_slug = await ensure_unique_slug(self.session, Category, base_slug)

        create_data = body.model_dump(exclude_unset=True)
        create_data["slug"] = unique_slug

        category = Category(**create_data)

        self.session.add(category)
        await self.session.flush()
        return category

    async def update(self, category_id: UUID, body: CategoryUpdateSchema) -> Category | None:
        """
        Обновляет категорию по её ID
        """
        category = await self.get_by_id(category_id)
        if not category:
            raise NoResultFound("Категория не найдена")

        update_data = body.model_dump(exclude_unset=True)

        if not update_data:
            raise NoResultFound("Нет данных для обновления")

        # Если изменилось название, обновляем slug
        if body.name:
            base_slug = generate_slug(body.name)
            unique_slug = await ensure_unique_slug(self.session, Category, base_slug, exclude_id=category_id)
            update_data["slug"] = unique_slug

        # Обновляем поля
        for key, value in update_data.items():
            setattr(category, key, value)

        await self.session.flush()
        return category

    async def delete(self, category_id: UUID) -> None:
        """
        Удаляет категорию по её ID
        """
        category = await self.get_by_id(category_id)

        if category:
            await self.session.delete(category)