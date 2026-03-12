"""
Сервис для работы с тегами
"""

import logging

from sqlalchemy.exc import NoResultFound, IntegrityError

from src.exceptions.base import BaseException, NotFoundException
from src.repositories.uow import UnitOfWork
from src.schemas.pagination import PaginatedResponse
from src.schemas.post import TagSchema
from src.schemas.tag import (
    TagQueryParams,
    TagCreateSchema,
    TagUpdateSchema,
    )

logger = logging.getLogger(__name__)


class TagService:

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_all(self, params: TagQueryParams) -> PaginatedResponse[TagSchema]:
        """
        Выдаёт пагинированную информацию о всех тегах
        """
        async with self.uow:
            tags, total = await self.uow.tag.get_all(params)

        items = [TagSchema.model_validate(tag) for tag in tags]

        return PaginatedResponse[TagSchema](
            items=items,
            total=total,
            limit=params.limit,
            offset=params.offset,
            has_next=(params.offset + 1) * params.limit < total,
            has_previous=params.offset > 0
        )

    async def get_by_id(self, tag_id: int) -> TagSchema:
        """
        Выдаёт информацию о теге по его ID
        """
        async with self.uow:
            tag = await self.uow.tag.get_by_id(tag_id)

            if not tag:
                raise NotFoundException(f"Тег с ID {tag_id} не найден")

        return TagSchema.model_validate(tag)

    async def get_by_slug(self, slug: str) -> TagSchema:
        """
        Выдаёт информацию о теге по его slug
        """
        async with self.uow:
            tag = await self.uow.tag.get_by_slug(slug)

            if not tag:
                raise NotFoundException(f"Тег с slug '{slug}' не найден")

        return TagSchema.model_validate(tag)

    async def create(self, body: TagCreateSchema) -> TagSchema:
        """
        Создаёт тег
        """
        async with self.uow:
            try:
                created_tag = await self.uow.tag.create(body)

            except IntegrityError as e:
                raise BaseException("Ошибка ограничения целостности данных в базе данных") from e

        return TagSchema.model_validate(created_tag)

    async def update(self, tag_id: int, body: TagUpdateSchema) -> TagSchema:
        """
        Обновляет содержимое тега
        """
        async with self.uow:
            try:
                updated_tag = await self.uow.tag.update(tag_id, body)
            except NoResultFound as e:
                raise BaseException("Нет данных для обновления") from e

            if not updated_tag:
                raise NotFoundException(f"Тег с ID {tag_id} не найден")

        return TagSchema.model_validate(updated_tag)

    async def delete(self, tag_id: int) -> None:
        """
        Удаляет тег
        """
        async with self.uow:
            tag = await self.uow.tag.get_by_id(tag_id)

            if not tag:
                raise NotFoundException(f"Тег с ID {tag_id} не найден")

            await self.uow.tag.delete(tag_id)