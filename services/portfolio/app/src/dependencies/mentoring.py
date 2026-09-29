from typing import Annotated

from fastapi import Depends

from src.dependencies.uow import get_unit_of_work
from src.repositories.uow import UnitOfWork
from src.services.mentoring import MentoringService


async def get_mentoring_service(
    uow: Annotated[UnitOfWork, Depends(get_unit_of_work)],
) -> MentoringService:
    """
    Возвращает сервис наставничества
    """
    return MentoringService(uow)
