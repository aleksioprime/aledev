from abc import ABC, abstractmethod
from uuid import UUID
import logging

from sqlalchemy.exc import NoResultFound
from sqlalchemy import update, delete, select, func, or_
from sqlalchemy.orm import selectinload

from src.models.post import Post, Category, Tag
from src.repositories.base import BaseSQLRepository
from src.schemas.post import (
    PostQueryParams,
    PostCreateSchema,
    PostUpdateSchema,
    PostOrderSchema,
    )
from src.utils.slug import generate_slug, ensure_unique_slug

logger = logging.getLogger(__name__)


class BasePostRepository(ABC):

    @abstractmethod
    async def get_by_id(self, post_id: UUID):
        ...

    @abstractmethod
    async def get_by_slug(self, slug: str):
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

    @abstractmethod
    async def get_or_create_category(self, category_slug: str):
        ...

    @abstractmethod
    async def get_or_create_tag(self, tag_name: str):
        ...


class PostRepository(BasePostRepository, BaseSQLRepository):

    async def get_by_id(self, post_id: UUID) -> Post | None:
        """
        Получает пост по его ID
        """
        stmt = select(Post).options(
            selectinload(Post.category),
            selectinload(Post.tags)
        ).where(Post.id == post_id)
        result = await self.session.execute(stmt)
        return result.scalars().unique().one_or_none()

    async def get_by_slug(self, slug: str) -> Post | None:
        """
        Получает пост по его slug
        """
        stmt = select(Post).options(
            selectinload(Post.category),
            selectinload(Post.tags)
        ).where(Post.slug == slug)
        result = await self.session.execute(stmt)
        return result.scalars().unique().one_or_none()

    async def get_all(self, params: PostQueryParams) -> tuple[list[Post], int]:
        """ Получает пагинированный список всех постов и количество записей"""
        stmt = select(Post).options(
            selectinload(Post.category),
            selectinload(Post.tags)
        )
        count_stmt = select(func.count()).select_from(Post)

        stmt = stmt.order_by(Post.order).limit(params.limit).offset(params.offset)

        result = await self.session.execute(stmt)
        posts = result.scalars().unique().all()

        total = (await self.session.execute(count_stmt)).scalar_one()
        return posts, total

    async def create(self, body: PostCreateSchema) -> Post:
        """ Создаёт новый пост """

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

        # Генерируем slug из заголовка
        base_slug = generate_slug(body.title)
        unique_slug = await ensure_unique_slug(self.session, Post, base_slug)

        # Получаем категорию если указана
        category = None
        if body.category_slug:
            category = await self.get_or_create_category(body.category_slug)

        # Получаем или создаем теги
        tags = []
        for tag_name in body.tags:
            tag = await self.get_or_create_tag(tag_name)
            tags.append(tag)

        # Подготавливаем данные для создания поста
        create_data = body.model_dump(exclude_unset=True, exclude={"category_slug", "tags"})
        create_data["order"] = order
        create_data["slug"] = unique_slug
        create_data["category_id"] = category.id if category else None

        post = Post(**create_data)
        post.tags = tags

        self.session.add(post)
        await self.session.flush()

        # Обновляем объект с загруженными связями
        await self.session.refresh(post, ['category', 'tags'])
        return post

    async def update(self, post_id: UUID, body: PostUpdateSchema) -> Post | None:
        """ Обновляет пост по его ID """
        # Получаем текущий пост
        post = await self.get_by_id(post_id)
        if not post:
            raise NoResultFound("Пост не найден")

        old_order = post.order
        new_order = body.order if body.order is not None else old_order

        # Обрабатываем изменение порядка
        if new_order != old_order:
            if new_order > old_order:
                # Сдвигаем все посты между old_order+1 и new_order включительно на -1
                await self.session.execute(
                    update(Post)
                    .where(Post.order > old_order, Post.order <= new_order)
                    .values(order=Post.order - 1)
                )
            else:
                # Сдвигаем все посты между new_order и old_order-1 на +1
                await self.session.execute(
                    update(Post)
                    .where(Post.order >= new_order, Post.order < old_order)
                    .values(order=Post.order + 1)
                )

        # Подготавливаем данные для обновления
        update_data = body.model_dump(exclude_unset=True, exclude={"category_slug", "tags"})

        if not update_data and body.category_slug is None and body.tags is None:
            raise NoResultFound("Нет данных для обновления")

        update_data["order"] = new_order

        # Если изменился заголовок, обновляем slug
        if body.title:
            base_slug = generate_slug(body.title)
            unique_slug = await ensure_unique_slug(self.session, Post, base_slug, exclude_id=post_id)
            update_data["slug"] = unique_slug

        # Обрабатываем категорию
        if body.category_slug is not None:
            if body.category_slug:
                category = await self.get_or_create_category(body.category_slug)
                update_data["category_id"] = category.id if category else None
            else:
                update_data["category_id"] = None

        # Обновляем основные поля
        if update_data:
            stmt = (
                update(Post)
                .where(Post.id == post_id)
                .values(**update_data)
                .execution_options(synchronize_session="fetch")
            )
            await self.session.execute(stmt)

        # Обрабатываем теги отдельно
        if body.tags is not None:
            # Очищаем старые теги
            post.tags.clear()

            # Добавляем новые теги
            for tag_name in body.tags:
                tag = await self.get_or_create_tag(tag_name)
                post.tags.append(tag)

            await self.session.flush()

        # Обновляем объект с загруженными связями
        await self.session.refresh(post, ['category', 'tags'])
        return post

    async def delete(self, post_id: UUID) -> None:
        """ Удаляет пост по его ID """
        post = await self.get_by_id(post_id)

        if post:
            await self.session.delete(post)

    async def reorder(self, items: list[PostOrderSchema]) -> None:
        """
        Массово обновляет поле order для постов.
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

    async def get_or_create_category(self, category_slug: str) -> Category | None:
        """
        Получает или создает категорию по slug
        """
        if not category_slug:
            return None

        # Сначала пытаемся найти существующую категорию
        stmt = select(Category).where(Category.slug == category_slug)
        result = await self.session.execute(stmt)
        category = result.scalars().unique().one_or_none()

        if category:
            return category

        # Если не найдена, возвращаем None (не создаем автоматически)
        return None

    async def get_or_create_tag(self, tag_name: str) -> Tag:
        """
        Получает или создает тег по имени/slug
        """
        # Пытаемся найти по имени или slug
        stmt = select(Tag).where(or_(Tag.name == tag_name, Tag.slug == tag_name))
        result = await self.session.execute(stmt)
        tag = result.scalars().unique().one_or_none()

        if tag:
            return tag

        # Создаем новый тег
        tag_slug = generate_slug(tag_name)
        tag_slug = await ensure_unique_slug(self.session, Tag, tag_slug)

        tag = Tag(name=tag_name, slug=tag_slug)
        self.session.add(tag)
        await self.session.flush()
        return tag