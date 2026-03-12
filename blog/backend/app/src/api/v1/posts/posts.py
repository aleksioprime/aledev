"""
Модуль с эндпоинтами для управления проектами
"""

from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Depends
from starlette import status

from src.schemas.security import UserJWT
from src.dependencies.post import get_post_service, get_post_params
from src.dependencies.security import permission_required
from src.schemas.pagination import PaginatedResponse
from src.schemas.post import (
    PostQueryParams,
    PostSchema,
    PostCreateSchema,
    PostUpdateSchema,
    PostOrderSchema
    )
from src.services.post import PostService

router = APIRouter()


@router.get(
    path='/',
    summary='Получить все посты',
    response_model=PaginatedResponse[PostSchema],
    status_code=status.HTTP_200_OK,
)
async def get_all_posts(
        params: Annotated[PostQueryParams, Depends(get_post_params)],
        service: Annotated[PostService, Depends(get_post_service)],
) -> PaginatedResponse[PostSchema]:
    """
    Возвращает пагинированный список всех постов
    """
    posts = await service.get_all(params)
    return posts


@router.get(
    path='/slug/{slug}/',
    summary='Получить пост по slug (публичный доступ)',
    response_model=PostSchema,
    status_code=status.HTTP_200_OK,
)
async def get_post_by_slug(
    slug: str,
    service: Annotated[PostService, Depends(get_post_service)],
):
    """
    Возвращает полное содержимое поста по его slug
    """
    post = await service.get_by_slug(slug)
    return post


@router.get(
    path='/{post_id}/',
    summary='Получить пост по его ID (админ)',
    response_model=PostSchema,
    status_code=status.HTTP_200_OK,
)
async def get_detailed_post(
    post_id: UUID,
    service: Annotated[PostService, Depends(get_post_service)],
    user: Annotated[UserJWT, Depends(permission_required())],
):
    """
    Возвращает полное содержимое поста по ID (для админов)
    """
    post = await service.get_by_id(post_id)
    return post


@router.post(
    path='/',
    summary='Создаёт пост',
    status_code=status.HTTP_201_CREATED,
    response_model=PostSchema,
)
async def create_post(
        body: PostCreateSchema,
        service: Annotated[PostService, Depends(get_post_service)],
        user: Annotated[UserJWT, Depends(permission_required(roles=["admin"]))],
) -> PostSchema:
    """
    Создаёт новый пост
    """
    post = await service.create(body)
    return post


@router.patch(
    path='/{post_id}/',
    summary='Обновление поста',
    response_model=PostSchema,
    status_code=status.HTTP_200_OK,
)
async def update_post(
    post_id: UUID,
    body: PostUpdateSchema,
    service: Annotated[PostService, Depends(get_post_service)],
    user: Annotated[UserJWT, Depends(permission_required(roles=["admin"]))],
):
    """
    Обновляет содержимое поста
    """
    post = await service.update(post_id, body=body)
    return post


@router.delete(
    path='/{post_id}/',
    summary='Удаление поста',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_post(
    post_id: UUID,
    service: Annotated[PostService, Depends(get_post_service)],
    user: Annotated[UserJWT, Depends(permission_required(roles=["admin"]))],
):
    """
    Удаляет пост
    """
    await service.delete(post_id)


@router.post(
    path='/reorder/',
    summary='Изменить порядок постов',
    status_code=status.HTTP_200_OK,
)
async def reorder_projects(
    body: List[PostOrderSchema],
    service: Annotated[PostService, Depends(get_post_service)],
    user: Annotated[UserJWT, Depends(permission_required(roles=["admin"]))],
):
    """
    Массово обновляет порядок постов
    """
    await service.reorder(body)
    return {"success": True}