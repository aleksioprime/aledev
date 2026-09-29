from typing import Annotated

from fastapi import Depends, Query

from src.dependencies.pagination import get_pagination_params
from src.dependencies.uow import get_unit_of_work
from src.repositories.uow import UnitOfWork
from src.schemas.achievement import AchievementQueryParams
from src.schemas.pagination import BasePaginationParams
from src.services.achievement import AchievementService


def get_achievement_params(
    pagination: Annotated[BasePaginationParams, Depends(get_pagination_params)],
    category: str | None = Query(None, max_length=40),
    scope: str | None = Query(None, max_length=30),
) -> AchievementQueryParams:
    """
    Собирает параметры фильтрации и пагинации достижений
    """
    return AchievementQueryParams(
        limit=pagination.limit,
        offset=pagination.offset,
        category=category,
        scope=scope,
    )


async def get_achievement_service(
    uow: Annotated[UnitOfWork, Depends(get_unit_of_work)],
) -> AchievementService:
    """
    Возвращает сервис достижений
    """
    return AchievementService(uow)
