from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response
from starlette import status

from src.constants.base import LangEnum
from src.dependencies.security import permission_required
from src.dependencies.uow import get_unit_of_work
from src.repositories.uow import UnitOfWork
from src.schemas.security import UserJWT
from src.services.export import PortfolioExportService

router = APIRouter()

DOCX_MEDIA_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


@router.get(
    "/portfolio/",
    summary="Экспорт портфолио в Word",
    status_code=status.HTTP_200_OK,
    response_class=Response,
    responses={200: {"content": {DOCX_MEDIA_TYPE: {}}}},
)
async def export_portfolio(
    uow: Annotated[UnitOfWork, Depends(get_unit_of_work)],
    user: Annotated[UserJWT, Depends(permission_required(roles=["admin"]))],
    lang: Annotated[LangEnum, Query(description="Язык документа")] = LangEnum.ru,
) -> Response:
    content = await PortfolioExportService(uow).build_docx(lang.value)
    filename = f"Semochkin_portfolio_{lang.value}.docx"
    return Response(
        content=content,
        media_type=DOCX_MEDIA_TYPE,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
