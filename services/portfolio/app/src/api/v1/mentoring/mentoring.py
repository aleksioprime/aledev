from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from src.dependencies.mentoring import get_mentoring_service
from src.dependencies.security import permission_required
from src.schemas.mentoring import MentoringPageSchema, MentoringPageUpdateSchema
from src.schemas.security import UserJWT
from src.services.mentoring import MentoringService

router = APIRouter()


@router.get(
    "/",
    summary="Контент секции наставничества",
    response_model=MentoringPageSchema,
    status_code=status.HTTP_200_OK,
)
async def get_mentoring_page(
    service: Annotated[MentoringService, Depends(get_mentoring_service)],
) -> MentoringPageSchema:
    return await service.get_page()


@router.get(
    "/admin/",
    summary="Контент секции наставничества для администрирования",
    response_model=MentoringPageSchema,
    status_code=status.HTTP_200_OK,
)
async def get_admin_mentoring_page(
    service: Annotated[MentoringService, Depends(get_mentoring_service)],
    user: Annotated[UserJWT, Depends(permission_required(roles=["admin"]))],
) -> MentoringPageSchema:
    return await service.get_page(include_unpublished=True)


@router.put(
    "/",
    summary="Обновить контент секции наставничества",
    response_model=MentoringPageSchema,
    status_code=status.HTTP_200_OK,
)
async def update_mentoring_page(
    body: MentoringPageUpdateSchema,
    service: Annotated[MentoringService, Depends(get_mentoring_service)],
    user: Annotated[UserJWT, Depends(permission_required(roles=["admin"]))],
) -> MentoringPageSchema:
    return await service.update_page(body)
