"""
Модуль с эндпоинтами обратной связи: публичная форма и управление обращениями в админке
"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, status, HTTPException, Request

from src.dependencies.feedback import get_feedback_service, get_feedback_params
from src.dependencies.security import permission_required
from src.schemas.feedback import (
    FeedbackCreateSchema,
    FeedbackQueryParams,
    FeedbackSchema,
    FeedbackStatsSchema,
    FeedbackUpdateSchema,
)
from src.schemas.pagination import PaginatedResponse
from src.schemas.security import UserJWT
from src.services.feedback import FeedbackService

router = APIRouter()


def _client_ip(request: Request) -> str | None:
    # Сервис доступен только через nginx, который выставляет X-Real-IP
    return request.headers.get("x-real-ip") or (request.client.host if request.client else None)


@router.post(
    "/",
    summary="Отправить обратную связь (заказ или вопрос)",
    status_code=status.HTTP_202_ACCEPTED,
)
async def send_feedback(
    body: FeedbackCreateSchema,
    request: Request,
    background_tasks: BackgroundTasks,
    service: Annotated[FeedbackService, Depends(get_feedback_service)],
):
    """
    Принимает обращение с сайта и ставит письмо в отправку
    """
    remote_ip = _client_ip(request)
    is_human = await service.verify_feedback_request(
        captcha_token=body.captcha_token,
        honeypot=body.website,
        form_started_at=body.form_started_at,
        remote_ip=remote_ip,
    )
    if not is_human:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Spam protection validation failed",
        )

    # Сначала сохраняем в БД - обращение не потеряется, даже если почта недоступна
    feedback_id = await service.create(body, ip=remote_ip, user_agent=request.headers.get("user-agent"))
    # Письмо уходит после ответа клиенту; при сбое его дошлёт воркер повторов
    background_tasks.add_task(service.notify, feedback_id)
    return {"message": "Обратная связь отправлена!", "id": str(feedback_id)}


@router.get(
    "/",
    summary="Список обращений",
    response_model=PaginatedResponse[FeedbackSchema],
)
async def list_feedback(
    params: Annotated[FeedbackQueryParams, Depends(get_feedback_params)],
    service: Annotated[FeedbackService, Depends(get_feedback_service)],
    user: Annotated[UserJWT, Depends(permission_required(roles=["admin"]))],
):
    """
    Возвращает список обращений
    """
    return await service.get_all(params)


@router.get(
    "/stats/",
    summary="Счётчики обращений",
    response_model=FeedbackStatsSchema,
)
async def feedback_stats(
    service: Annotated[FeedbackService, Depends(get_feedback_service)],
    user: Annotated[UserJWT, Depends(permission_required(roles=["admin"]))],
):
    """
    Возвращает счётчики обращений
    """
    return await service.stats()


@router.patch(
    "/{feedback_id}/",
    summary="Изменить статус / заметку обращения",
    response_model=FeedbackSchema,
)
async def update_feedback(
    feedback_id: UUID,
    body: FeedbackUpdateSchema,
    service: Annotated[FeedbackService, Depends(get_feedback_service)],
    user: Annotated[UserJWT, Depends(permission_required(roles=["admin"]))],
):
    """
    Меняет статус или заметку обращения
    """
    return await service.update(feedback_id, body)


@router.post(
    "/{feedback_id}/resend/",
    summary="Повторно отправить письмо по обращению",
    response_model=FeedbackSchema,
)
async def resend_feedback(
    feedback_id: UUID,
    service: Annotated[FeedbackService, Depends(get_feedback_service)],
    user: Annotated[UserJWT, Depends(permission_required(roles=["admin"]))],
):
    """
    Повторно отправляет письмо по обращению
    """
    return await service.requeue(feedback_id)


@router.delete(
    "/{feedback_id}/",
    summary="Удалить обращение",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_feedback(
    feedback_id: UUID,
    service: Annotated[FeedbackService, Depends(get_feedback_service)],
    user: Annotated[UserJWT, Depends(permission_required(roles=["admin"]))],
):
    """
    Удаляет обращение
    """
    await service.delete(feedback_id)
