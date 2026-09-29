import time
from collections import defaultdict, deque
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from starlette import status

from src.constants.base import LangEnum
from src.dependencies.uow import get_unit_of_work
from src.repositories.uow import UnitOfWork
from src.services.export import PortfolioExportService

router = APIRouter()

DOCX_MEDIA_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

# Готовый документ кэшируется, скачивания ограничены по IP
CACHE_TTL = 60
RATE_LIMIT, RATE_WINDOW = 10, 60
_cache: dict[str, tuple[float, bytes]] = {}
_hits: dict[str, deque[float]] = defaultdict(deque)


def _client_ip(request: Request) -> str:
    """
    IP посетителя из заголовка nginx
    """
    return request.headers.get("x-real-ip") or (request.client.host if request.client else "unknown")


def _check_rate(ip: str) -> None:
    """
    Отклоняет запрос, если с IP скачивали слишком часто
    """
    now = time.monotonic()
    hits = _hits[ip]
    while hits and now - hits[0] > RATE_WINDOW:
        hits.popleft()
    if len(hits) >= RATE_LIMIT:
        raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, "Слишком много запросов, попробуйте позже")
    hits.append(now)


@router.get(
    "/portfolio/",
    summary="Экспорт портфолио в Word",
    status_code=status.HTTP_200_OK,
    response_class=Response,
    responses={200: {"content": {DOCX_MEDIA_TYPE: {}}}},
)
async def export_portfolio(
    request: Request,
    uow: Annotated[UnitOfWork, Depends(get_unit_of_work)],
    lang: Annotated[LangEnum, Query(description="Язык документа")] = LangEnum.ru,
) -> Response:
    """
    Отдаёт портфолио в формате Word
    """
    _check_rate(_client_ip(request))

    cached = _cache.get(lang.value)
    if cached and time.monotonic() - cached[0] < CACHE_TTL:
        content = cached[1]
    else:
        content = await PortfolioExportService(uow).build_docx(lang.value)
        _cache[lang.value] = (time.monotonic(), content)

    filename = f"Semochkin_portfolio_{lang.value}.docx"
    return Response(
        content=content,
        media_type=DOCX_MEDIA_TYPE,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
