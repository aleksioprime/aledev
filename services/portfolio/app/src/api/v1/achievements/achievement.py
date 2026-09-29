from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Response
from starlette import status

from src.dependencies.achievement import get_achievement_params, get_achievement_service
from src.dependencies.security import permission_required
from src.schemas.achievement import (
    AchievementCreateSchema,
    AchievementQueryParams,
    AchievementSchema,
    AchievementUpdateSchema,
)
from src.schemas.pagination import PaginatedResponse
from src.schemas.security import UserJWT
from src.services.achievement import AchievementService

router = APIRouter()


@router.get(
    "/",
    summary="Список опубликованных достижений",
    response_model=PaginatedResponse[AchievementSchema],
    status_code=status.HTTP_200_OK,
)
async def get_achievements(
    params: Annotated[AchievementQueryParams, Depends(get_achievement_params)],
    service: Annotated[AchievementService, Depends(get_achievement_service)],
) -> PaginatedResponse[AchievementSchema]:
    return await service.get_all(params)


@router.get(
    "/admin/",
    summary="Список достижений для администрирования",
    response_model=PaginatedResponse[AchievementSchema],
    status_code=status.HTTP_200_OK,
)
async def get_admin_achievements(
    params: Annotated[AchievementQueryParams, Depends(get_achievement_params)],
    service: Annotated[AchievementService, Depends(get_achievement_service)],
    user: Annotated[UserJWT, Depends(permission_required(roles=["admin"]))],
) -> PaginatedResponse[AchievementSchema]:
    return await service.get_all(params, include_unpublished=True)


@router.post(
    "/",
    summary="Создать достижение",
    response_model=AchievementSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_achievement(
    body: AchievementCreateSchema,
    service: Annotated[AchievementService, Depends(get_achievement_service)],
    user: Annotated[UserJWT, Depends(permission_required(roles=["admin"]))],
) -> AchievementSchema:
    return await service.create(body)


@router.patch(
    "/{achievement_id}/",
    summary="Обновить достижение",
    response_model=AchievementSchema,
    status_code=status.HTTP_200_OK,
)
async def update_achievement(
    achievement_id: UUID,
    body: AchievementUpdateSchema,
    service: Annotated[AchievementService, Depends(get_achievement_service)],
    user: Annotated[UserJWT, Depends(permission_required(roles=["admin"]))],
) -> AchievementSchema:
    return await service.update(achievement_id, body)


@router.delete(
    "/{achievement_id}/",
    summary="Удалить достижение",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_achievement(
    achievement_id: UUID,
    service: Annotated[AchievementService, Depends(get_achievement_service)],
    user: Annotated[UserJWT, Depends(permission_required(roles=["admin"]))],
) -> Response:
    await service.delete(achievement_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
