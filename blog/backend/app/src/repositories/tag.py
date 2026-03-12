"""
Репозиторий для работы с тегами
"""

from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy import select, func, or_
from sqlalchemy.exc import NoResultFound

from src.models.post import Tag
from src.repositories.base import BaseSQLRepository
from src.schemas.tag import TagCreateSchema, TagUpdateSchema, TagQueryParams
from src.utils.slug import generate_slug, ensure_unique_slug


class BaseTagRepository(ABC):

    @abstractmethod
    async def get_by_id(self, tag_id: int):
        ...

    @abstractmethod
    async def get_by_slug(self, slug: str):
        ...

    @abstractmethod
    async def get_all(self, params: TagQueryParams):
        ...

    @abstractmethod
    async def create(self, body: TagCreateSchema):
        ...

    @abstractmethod
    async def update(self, tag_id: int, body: TagUpdateSchema):
        ...

    @abstractmethod
    async def delete(self, tag_id: int):
        ...


class TagRepository(BaseTagRepository, BaseSQLRepository):

    async def get_by_id(self, tag_id: int) -> Tag | None:
        """
        Получает тег по его ID
        """
        stmt = select(Tag).where(Tag.id == tag_id)
        result = await self.session.execute(stmt)
        return result.scalars().unique().one_or_none()

    async def get_by_slug(self, slug: str) -> Tag | None:
        """
        Получает тег по его slug
        """
        stmt = select(Tag).where(Tag.slug == slug)
        result = await self.session.execute(stmt)
        return result.scalars().unique().one_or_none()

    async def get_all(self, params: TagQueryParams) -> tuple[list[Tag], int]:
        """
        Получает пагинированный список тегов
        """
        stmt = select(Tag)
        count_stmt = select(func.count()).select_from(Tag)

        # Поиск по названию
        if params.search:
            search_pattern = f"%{params.search}%"
            stmt = stmt.where(or_(
                Tag.name.ilike(search_pattern),
                Tag.slug.ilike(search_pattern)
            ))
            count_stmt = count_stmt.where(or_(
                Tag.name.ilike(search_pattern),
                Tag.slug.ilike(search_pattern)
            ))

        stmt = stmt.order_by(Tag.name).limit(params.limit).offset(params.offset)

        result = await self.session.execute(stmt)
        tags = result.scalars().unique().all()

        total = (await self.session.execute(count_stmt)).scalar_one()
        return tags, total

    async def create(self, body: TagCreateSchema) -> Tag:
        """
        Создаёт новый тег
        """
        # Генерируем slug из названия
        base_slug = generate_slug(body.name)
        unique_slug = await ensure_unique_slug(self.session, Tag, base_slug)

        create_data = body.model_dump(exclude_unset=True)
        create_data["slug"] = unique_slug

        tag = Tag(**create_data)

        self.session.add(tag)
        await self.session.flush()
        return tag

    async def update(self, tag_id: int, body: TagUpdateSchema) -> Tag | None:
        """
        Обновляет тег по его ID
        """
        tag = await self.get_by_id(tag_id)
        if not tag:
            raise NoResultFound("Тег не найден")

        update_data = body.model_dump(exclude_unset=True)

        if not update_data:
            raise NoResultFound("Нет данных для обновления")

        # Если изменилось название, обновляем slug
        if body.name:
            base_slug = generate_slug(body.name)
            unique_slug = await ensure_unique_slug(self.session, Tag, base_slug, exclude_id=tag_id)
            update_data["slug"] = unique_slug

        # Обновляем поля
        for key, value in update_data.items():
            setattr(tag, key, value)

        await self.session.flush()
        return tag

    async def delete(self, tag_id: int) -> None:
        """
        Удаляет тег по его ID
        """
        tag = await self.get_by_id(tag_id)

        if tag:
            await self.session.delete(tag)