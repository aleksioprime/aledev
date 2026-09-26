"""
Модуль с эндпоинтами для управления проектами
"""

from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Depends
from starlette import status

from src.constants.base import LangEnum
from src.schemas.security import UserJWT
from src.dependencies.project import get_project_service, get_project_params
from src.dependencies.security import permission_required
from src.schemas.pagination import PaginatedResponse
from src.schemas.project import (
    ProjectQueryParams,
    ProjectSchema,
    ProjectCreateSchema,
    ProjectUpdateSchema,
    ProjectTranslationSchema,
    ProjectTranslationCreateSchema,
    ProjectTranslationUpdateSchema,
    ProjectOrderSchema
    )
from src.services.project import ProjectService

router = APIRouter()


@router.get(
    path='/',
    summary='Получить все проекты',
    response_model=PaginatedResponse[ProjectSchema],
    status_code=status.HTTP_200_OK,
)
async def get_all_projects(
        params: Annotated[ProjectQueryParams, Depends(get_project_params)],
        service: Annotated[ProjectService, Depends(get_project_service)],
) -> PaginatedResponse[ProjectSchema]:
    """
    Возвращает пагинированный список всех проектов
    """
    projects = await service.get_all(params)
    return projects


@router.get(
    path='/{project_id}/',
    summary='Получить информацию о проекте',
    response_model=ProjectSchema,
    status_code=status.HTTP_200_OK,
)
async def get_detailed_project(
    project_id: UUID,
    service: Annotated[ProjectService, Depends(get_project_service)],
    user: Annotated[UserJWT, Depends(permission_required())],
):
    """
    Возвращает детальную информацию о выбранном проекте
    """
    project = await service.get_by_id(project_id)
    return project


@router.post(
    path='/',
    summary='Создаёт проект',
    status_code=status.HTTP_201_CREATED,
    response_model=ProjectSchema,
)
async def create_project(
        body: ProjectCreateSchema,
        service: Annotated[ProjectService, Depends(get_project_service)],
        user: Annotated[UserJWT, Depends(permission_required(roles=["admin"]))],
) -> ProjectSchema:
    """
    Создаёт новый проект
    """
    project = await service.create(body)
    return project


@router.patch(
    path='/{project_id}/',
    summary='Обновление проекта',
    response_model=ProjectSchema,
    status_code=status.HTTP_200_OK,
)
async def update_project(
    project_id: UUID,
    body: ProjectUpdateSchema,
    service: Annotated[ProjectService, Depends(get_project_service)],
    user: Annotated[UserJWT, Depends(permission_required(roles=["admin"]))],
):
    """
    Обновляет информацию о проекте
    """
    project = await service.update(project_id, body=body)
    return project


@router.delete(
    path='/{project_id}/',
    summary='Удаление проекта',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_project(
    project_id: UUID,
    service: Annotated[ProjectService, Depends(get_project_service)],
    user: Annotated[UserJWT, Depends(permission_required(roles=["admin"]))],
):
    """
    Удаляет проект
    """
    await service.delete(project_id)


@router.post(
    path='/{project_id}/translations/',
    summary='Добавить перевод к проекту',
    response_model=ProjectTranslationSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_project_translation(
    project_id: UUID,
    body: ProjectTranslationCreateSchema,
    service: Annotated[ProjectService, Depends(get_project_service)],
    user: Annotated[UserJWT, Depends(permission_required(roles=["admin"]))],
):
    """
    Добавляет новый перевод к проекту
    """
    translation = await service.add_translation(project_id, body)
    return translation


@router.patch(
    path='/{project_id}/translations/{lang}/',
    summary='Обновить перевод проекта',
    response_model=ProjectTranslationSchema,
    status_code=status.HTTP_200_OK,
)
async def update_project_translation(
    project_id: UUID,
    lang: LangEnum,
    body: ProjectTranslationUpdateSchema,
    service: Annotated[ProjectService, Depends(get_project_service)],
    user: Annotated[UserJWT, Depends(permission_required(roles=["admin"]))],
):
    """
    Обновляет перевод проекта по языку
    """
    translation = await service.update_translation(project_id, lang, body)
    return translation


@router.delete(
    path='/{project_id}/translations/{lang}/',
    summary='Удалить перевод проекта',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_project_translation(
    project_id: UUID,
    lang: LangEnum,
    service: Annotated[ProjectService, Depends(get_project_service)],
    user: Annotated[UserJWT, Depends(permission_required(roles=["admin"]))],
):
    """
    Удаляет перевод проекта по языку
    """
    await service.delete_translation(project_id, lang)


@router.post(
    path='/reorder/',
    summary='Изменить порядок проектов',
    status_code=status.HTTP_200_OK,
)
async def reorder_projects(
    body: List[ProjectOrderSchema],
    service: Annotated[ProjectService, Depends(get_project_service)],
    user: Annotated[UserJWT, Depends(permission_required(roles=["admin"]))],
):
    """
    Массово обновляет порядок проектов.
    """
    await service.reorder(body)
    return {"success": True}