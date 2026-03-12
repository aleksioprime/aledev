"""
Утилиты для работы со slug
"""

import re
import unidecode
from typing import TYPE_CHECKING, TypeVar
from sqlalchemy import select, func

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from src.models.post import Post, Category, Tag

T = TypeVar("T")  # универсальный тип ORM-модели


def generate_slug(text: str) -> str:
    """
    Генерирует slug из текста.
    """
    slug = unidecode.unidecode(text)      # Транслитерация
    slug = slug.lower()                   # Приведение к нижнему регистру
    slug = re.sub(r"[^\w\s-]", "", slug)  # Удаляем лишние символы
    slug = re.sub(r"[-\s]+", "-", slug)   # Пробелы и дефисы объединяем
    slug = slug.strip("-")                # Убираем крайние дефисы
    return slug


async def ensure_unique_slug(
    session: "AsyncSession",
    model: type[T],
    base_slug: str,
    exclude_id: str | int | None = None,
) -> str:
    """
    Обеспечивает уникальность slug, добавляя номер если необходимо.
    """
    original_slug = base_slug
    counter = 1

    while True:
        stmt = select(func.count()).select_from(model).where(model.slug == base_slug)

        if exclude_id is not None:
            stmt = stmt.where(model.id != exclude_id)

        count = await session.scalar(stmt)

        if count == 0:
            return base_slug

        counter += 1
        base_slug = f"{original_slug}-{counter}"
