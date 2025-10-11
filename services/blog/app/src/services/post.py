import logging
from uuid import UUID

from sqlalchemy.exc import NoResultFound, IntegrityError

from src.exceptions.base import BaseException, NotFoundException
from src.repositories.uow import UnitOfWork
from src.schemas.pagination import PaginatedResponse
from src.schemas.post import (
    PostQueryParams,
    PostSchema,
    PostCreateSchema,
    PostUpdateSchema,
    PostOrderSchema,
    )

logger = logging.getLogger(__name__)


class PostService:

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_all(self, params: PostQueryParams) -> PaginatedResponse[PostSchema]:
        """
        Выдаёт пагинированную информацию обо всех постах
        """
        async with self.uow:
            posts, total = await self.uow.post.get_all(params)

        items = [PostSchema.model_validate(post) for post in posts]

        return PaginatedResponse[PostSchema](
            items=items,
            total=total,
            limit=params.limit,
            offset=params.offset,
            has_next=(params.offset + 1) * params.limit < total,
            has_previous=params.offset > 0
        )

    async def get_by_id(self, post_id: UUID) -> PostSchema:
        """
        Выдаёт информацию о посте по его ID
        """
        async with self.uow:
            post = await self.uow.post.get_by_id(post_id)

            if not post:
                raise NotFoundException(f"Пост с ID {post_id} не найден")

        return post

    async def create(self, body: PostCreateSchema) -> PostSchema:
        """
        Создаёт пост
        """
        async with self.uow:
            try:
                created_post = await self.uow.post.create(body)

            except IntegrityError as e:
                raise BaseException("Ошибка ограничения целостности данных в базе данных") from e

        return created_post

    async def update(self, post_id: UUID, body: PostUpdateSchema) -> PostSchema:
        """
        Обновляет содержимое поста
        """
        async with self.uow:
            try:
                updated_post = await self.uow.post.update(post_id, body)
            except NoResultFound as e:
                raise BaseException("Нет данных для обновления") from e

            if not updated_post:
                raise NotFoundException(f"Пост с ID {post_id} не найден")

        return updated_post

    async def delete(self, post_id: UUID) -> None:
        """
        Удаляет пост
        """
        async with self.uow:
            post = await self.uow.post.get_by_id(post_id)

            if not post:
                raise NotFoundException(f"Проект с ID  {post_id} не найден")

            await self.uow.post.delete(post_id)

    async def reorder(self, items: list[PostOrderSchema]) -> None:
        """
        Массово обновляет порядок постов
        """
        async with self.uow:
            await self.uow.project.reorder(items)