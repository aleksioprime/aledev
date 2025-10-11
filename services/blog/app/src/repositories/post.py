from abc import ABC, abstractmethod
from uuid import UUID
import logging

from sqlalchemy.exc import NoResultFound
from sqlalchemy import update, delete, select, func

from src.models.post import Post
from src.repositories.base import BaseSQLRepository
from src.schemas.post import (
    PostQueryParams,
    PostCreateSchema,
    PostUpdateSchema,
    PostOrderSchema,
    )

logger = logging.getLogger(__name__)


class BasePostRepository(ABC):

    @abstractmethod
    async def get_by_id(self, post_id: UUID):
        ...

    @abstractmethod
    async def get_all(self, params: PostQueryParams):
        ...

    @abstractmethod
    async def create(self, body: PostCreateSchema):
        ...

    @abstractmethod
    async def update(self, post_id: UUID, body: PostUpdateSchema):
        ...

    @abstractmethod
    async def delete(self, post_id: UUID):
        ...


class PostRepository(BasePostRepository, BaseSQLRepository):

    async def get_by_id(self, post_id: UUID) -> Post | None:
        """
        Получает проект по его ID
        """
        stmt = select(Post).where(Post.id == post_id)
        result = await self.session.execute(stmt)
        return result.scalars().unique().one_or_none()

    async def get_all(self, params: PostQueryParams) -> tuple[list[Post], int]:
        """ Получает пагинированный список всех проектов и количество записей"""
        stmt = select(Post)
        count_stmt = select(func.count()).select_from(Post)

        stmt = stmt.order_by(Post.order).limit(params.limit).offset(params.offset)

        result = await self.session.execute(stmt)
        posts = result.scalars().unique().all()

        total = (await self.session.execute(count_stmt)).scalar_one()
        return posts, total

    async def create(self, body: PostCreateSchema) -> Post:
        """ Создаёт новый проект """

        # Если явно передан order, надо сдвинуть остальных
        if body.order is not None:
            await self.session.execute(
                update(Post)
                .where(Post.order >= body.order)
                .values(order=Post.order + 1)
            )
            order = body.order
        else:
            max_order = (await self.session.execute(
                select(func.max(Post.order))
            )).scalar()
            order = (max_order or 0) + 1

        create_data = body.model_dump(exclude_unset=True, exclude={"translations"})
        create_data["order"] = order

        post = Post(**create_data)

        self.session.add(post)
        await self.session.flush()
        return post

    async def update(self, post_id: UUID, body: PostUpdateSchema) -> Post | None:
        """ Обновляет проект по его ID """
        # Получаем текущий order этого проекта
        post = await self.get_by_id(post_id)
        if not post:
            raise NoResultFound("Проект не найден")

        old_order = post.order
        new_order = body.order if body.order is not None else old_order

        if new_order != old_order:
            if new_order > old_order:
                # Сдвигаем все проекты между old_order+1 и new_order включительно на -1
                await self.session.execute(
                    update(Post)
                    .where(Post.order > old_order, Post.order <= new_order)
                    .values(order=Post.order - 1)
                )
            else:
                # Сдвигаем все проекты между new_order и old_order-1 на +1
                await self.session.execute(
                    update(Post)
                    .where(Post.order >= new_order, Post.order < old_order)
                    .values(order=Post.order + 1)
                )

        update_data = { key: value for key, value in body.dict(exclude_unset=True).items() }
        if not update_data:
            raise NoResultFound("Нет данных для обновления")

        update_data["order"] = new_order

        stmt = (
            update(Post)
            .where(Post.id == post_id)
            .values(**update_data)
            .execution_options(synchronize_session="fetch")
        )

        await self.session.execute(stmt)


        return await self.get_by_id(post_id)

    async def delete(self, post_id: UUID) -> None:
        """ Удаляет проект по его ID """
        post = await self.get_by_id(post_id)

        if post:
            await self.session.delete(post)

    async def reorder(self, items: list[PostOrderSchema]) -> None:
        """
        Массово обновляет поле order для проектов.
        """
        for item in items:
            stmt = (
                update(Post)
                .where(Post.id == item.id)
                .values(order=item.order)
                .execution_options(synchronize_session="fetch")
            )
            await self.session.execute(stmt)
        await self.session.flush()