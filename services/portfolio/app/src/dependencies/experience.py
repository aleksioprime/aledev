from typing import Annotated

from fastapi import Depends

from src.schemas.pagination import BasePaginationParams
from src.dependencies.pagination import get_pagination_params
from src.dependencies.uow import get_unit_of_work
from src.schemas.experience import ExperienceQueryParams
from src.repositories.uow import UnitOfWork
from src.services.experience import ExperienceService


def get_experience_params(
        pagination: Annotated[BasePaginationParams, Depends(get_pagination_params)],
) -> ExperienceQueryParams:
    """ Получает query-параметры фильтрации для опыта """

    return ExperienceQueryParams(
        limit=pagination.limit,
        offset=pagination.offset,
    )


async def get_experience_service(
        uow: Annotated[UnitOfWork, Depends(get_unit_of_work)],
):
    return ExperienceService(uow)