"""
Сервис для работы с категориями
"""

import logging
from uuid import UUID

from sqlalchemy.exc import NoResultFound, IntegrityError

from src.exceptions.base import BaseException, NotFoundException
from src.repositories.uow import UnitOfWork
from src.schemas.pagination import PaginatedResponse
from src.schemas.post import CategorySchema
from src.schemas.category import (
    CategoryQueryParams,
    CategoryCreateSchema,
    CategoryUpdateSchema,
    )

logger = logging.getLogger(__name__)


class CategoryService:

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_all(self, params: CategoryQueryParams) -> PaginatedResponse[CategorySchema]:
        """
        Выдаёт пагинированную информацию о всех категориях
        """
        async with self.uow:
            categories, total = await self.uow.category.get_all(params)

        items = [CategorySchema.model_validate(category) for category in categories]

        return PaginatedResponse[CategorySchema](
            items=items,
            total=total,
            limit=params.limit,
            offset=params.offset,
            has_next=(params.offset + 1) * params.limit < total,
            has_previous=params.offset > 0
        )

    async def get_by_id(self, category_id: UUID) -> CategorySchema:
        """
        Выдаёт информацию о категории по её ID
        """
        async with self.uow:
            category = await self.uow.category.get_by_id(category_id)

            if not category:
                raise NotFoundException(f"Категория с ID {category_id} не найдена")

        return CategorySchema.model_validate(category)

    async def get_by_slug(self, slug: str) -> CategorySchema:
        """
        Выдаёт информацию о категории по её slug
        """
        async with self.uow:
            category = await self.uow.category.get_by_slug(slug)

            if not category:
                raise NotFoundException(f"Категория с slug '{slug}' не найдена")

        return CategorySchema.model_validate(category)

    async def create(self, body: CategoryCreateSchema) -> CategorySchema:
        """
        Создаёт категорию
        """
        async with self.uow:
            try:
                created_category = await self.uow.category.create(body)

            except IntegrityError as e:
                raise BaseException("Ошибка ограничения целостности данных в базе данных") from e

        return CategorySchema.model_validate(created_category)

    async def update(self, category_id: UUID, body: CategoryUpdateSchema) -> CategorySchema:
        """
        Обновляет содержимое категории
        """
        async with self.uow:
            try:
                updated_category = await self.uow.category.update(category_id, body)
            except NoResultFound as e:
                raise BaseException("Нет данных для обновления") from e

            if not updated_category:
                raise NotFoundException(f"Категория с ID {category_id} не найдена")

        return CategorySchema.model_validate(updated_category)

    async def delete(self, category_id: UUID) -> None:
        """
        Удаляет категорию
        """
        async with self.uow:
            category = await self.uow.category.get_by_id(category_id)

            if not category:
                raise NotFoundException(f"Категория с ID {category_id} не найдена")

            await self.uow.category.delete(category_id)