from typing import Annotated

from fastapi import Query, Depends

from src.schemas.pagination import BasePaginationParams
from src.dependencies.pagination import get_pagination_params
from src.dependencies.uow import get_unit_of_work
from src.schemas.project import ProjectQueryParams
from src.repositories.uow import UnitOfWork
from src.services.project import ProjectService


def get_project_params(
        pagination: Annotated[BasePaginationParams, Depends(get_pagination_params)],
        is_favorite: bool | None = Query(None, description="Фильтрация изобранных проектов"),
) -> ProjectQueryParams:
    """ Получает query-параметры фильтрации для проектов """

    return ProjectQueryParams(
        limit=pagination.limit,
        offset=pagination.offset,
        is_favorite=is_favorite,
    )


async def get_project_service(
        uow: Annotated[UnitOfWork, Depends(get_unit_of_work)],
):
    return ProjectService(uow)