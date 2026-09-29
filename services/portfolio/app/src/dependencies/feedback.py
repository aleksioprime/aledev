from typing import Annotated

from fastapi import Depends, Query

from src.constants.base import FeedbackKind, FeedbackStatus
from src.core.config import settings
from src.dependencies.pagination import get_pagination_params
from src.schemas.feedback import FeedbackQueryParams
from src.schemas.pagination import BasePaginationParams
from src.services.feedback import FeedbackService


def get_feedback_service() -> FeedbackService:
    """
    Возвращает сервис обратной связи
    """
    return FeedbackService(settings.email, settings.feedback_protection)


def get_feedback_params(
        pagination: Annotated[BasePaginationParams, Depends(get_pagination_params)],
        kind: FeedbackKind | None = Query(None, description="Тип обращения"),
        status: FeedbackStatus | None = Query(None, description="Статус обработки"),
        search: str | None = Query(None, max_length=100, description="Поиск по имени, email, тексту"),
) -> FeedbackQueryParams:
    """
    Собирает параметры фильтрации и пагинации обращений
    """
    return FeedbackQueryParams(
        limit=pagination.limit,
        offset=pagination.offset,
        kind=kind,
        status=status,
        search=search or None,
    )
