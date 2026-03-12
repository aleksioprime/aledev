from typing import Annotated

from fastapi import Query, Depends

from src.schemas.pagination import BasePaginationParams
from src.dependencies.pagination import get_pagination_params
from src.dependencies.uow import get_unit_of_work
from src.schemas.post import PostQueryParams
from src.repositories.uow import UnitOfWork
from src.services.post import PostService


def get_post_params(
        pagination: Annotated[BasePaginationParams, Depends(get_pagination_params)],
) -> PostQueryParams:
    """ Получает query-параметры фильтрации для постов """

    return PostQueryParams(
        limit=pagination.limit,
        offset=pagination.offset,
    )


async def get_post_service(
        uow: Annotated[UnitOfWork, Depends(get_unit_of_work)],
):
    return PostService(uow)