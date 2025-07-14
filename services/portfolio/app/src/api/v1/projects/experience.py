"""
Модуль с эндпоинтами для управления опытом работы
"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from starlette import status

from src.constants.base import LangEnum

from src.schemas.security import UserJWT
from src.dependencies.experience import get_experience_service, get_experience_params
from src.dependencies.security import permission_required
from src.schemas.pagination import PaginatedResponse
from src.schemas.experience import (
    ExperienceQueryParams,
    ExperienceSchema,
    ExperienceCreateSchema,
    ExperienceUpdateSchema,
    ExperienceTranslationSchema,
    ExperienceTranslationCreateSchema,
    ExperienceTranslationUpdateSchema,
    )

from src.services.experience import ExperienceService

router = APIRouter()


@router.get(
    path='/',
    summary='Получить все записи об опыте работы',
    response_model=PaginatedResponse[ExperienceSchema],
    status_code=status.HTTP_200_OK,
)
async def get_all_experiences(
        params: Annotated[ExperienceQueryParams, Depends(get_experience_params)],
        service: Annotated[ExperienceService, Depends(get_experience_service)],
) -> PaginatedResponse[ExperienceSchema]:
    """
    Возвращает пагинированный список всех записей опыта работы
    """
    experiences = await service.get_all(params)
    return experiences


@router.get(
    path='/{experience_id}/',
    summary='Получить информацию о записи опыта работы',
    response_model=ExperienceSchema,
    status_code=status.HTTP_200_OK,
)
async def get_detailed_experience(
    experience_id: UUID,
    service: Annotated[ExperienceService, Depends(get_experience_service)],
    user: Annotated[UserJWT, Depends(permission_required())],
):
    """
    Возвращает детальную информацию о выбранном опыте работы
    """
    experience = await service.get_by_id(experience_id)
    return experience

@router.post(
    path='/',
    summary='Создаёт запись об опыте работы',
    status_code=status.HTTP_201_CREATED,
    response_model=ExperienceSchema,
)
async def create_experience(
        body: ExperienceCreateSchema,
        service: Annotated[ExperienceService, Depends(get_experience_service)],
        user: Annotated[UserJWT, Depends(permission_required(roles=["admin"]))],
) -> ExperienceSchema:
    """
    Создаёт новую запись об опыте работы
    """
    experience = await service.create(body)
    return experience


@router.patch(
    path='/{experience_id}/',
    summary='Обновление записи об опыте работы',
    response_model=ExperienceSchema,
    status_code=status.HTTP_200_OK,
)
async def update_experience(
    experience_id: UUID,
    body: ExperienceUpdateSchema,
    service: Annotated[ExperienceService, Depends(get_experience_service)],
    user: Annotated[UserJWT, Depends(permission_required(roles=["admin"]))],
):
    """
    Обновляет информацию записи об опыте работы
    """
    experience = await service.update(experience_id, body=body)
    return experience


@router.delete(
    path='/{experience_id}/',
    summary='Удаление записи об опыте работы',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_experience(
    experience_id: UUID,
    service: Annotated[ExperienceService, Depends(get_experience_service)],
    user: Annotated[UserJWT, Depends(permission_required(roles=["admin"]))],
):
    """
    Удаляет запись об опыте работы
    """
    await service.delete(experience_id)


@router.post(
    path='/{experience_id}/translations/',
    summary='Добавить перевод к проекту',
    response_model=ExperienceTranslationSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_experience_translation(
    experience_id: UUID,
    body: ExperienceTranslationCreateSchema,
    service: Annotated[ExperienceService, Depends(get_experience_service)],
    user: Annotated[UserJWT, Depends(permission_required(roles=["admin"]))],
):
    """
    Добавляет новый перевод к проекту
    """
    translation = await service.add_translation(experience_id, body)
    return translation


@router.patch(
    path='/{experience_id}/translations/{lang}/',
    summary='Обновить перевод проекта',
    response_model=ExperienceTranslationSchema,
    status_code=status.HTTP_200_OK,
)
async def update_experience_translation(
    experience_id: UUID,
    lang: LangEnum,
    body: ExperienceTranslationUpdateSchema,
    service: Annotated[ExperienceService, Depends(get_experience_service)],
    user: Annotated[UserJWT, Depends(permission_required(roles=["admin"]))],
):
    """
    Обновляет перевод проекта по языку
    """
    translation = await service.update_translation(experience_id, lang, body)
    return translation


@router.delete(
    path='/{experience_id}/translations/{lang}/',
    summary='Удалить перевод проекта',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_experience_translation(
    experience_id: UUID,
    lang: LangEnum,
    service: Annotated[ExperienceService, Depends(get_experience_service)],
    user: Annotated[UserJWT, Depends(permission_required(roles=["admin"]))],
):
    """
    Удаляет перевод проекта по языку
    """
    await service.delete_translation(experience_id, lang)