from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text

from src.db.postgres import get_db_session

router = APIRouter()


@router.get("/ping/", status_code=status.HTTP_200_OK)
async def ping():
    """
    Эндпоинт для проверки работы web-сервера
    """
    return {"status": "ok", "message": "Server is up and running"}


@router.get("/ping/postgres/", status_code=status.HTTP_200_OK)
async def postgres_health_check(db_session: AsyncSession = Depends(get_db_session)):
    """
    Эндпоинт для проверки состояния PostgreSQL
    """
    try:
        result = await db_session.execute(text("SELECT 1"))
        if result.scalar() == 1:
            return {"status": "ok", "message": "Postgres is operational"}
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"status": "error", "message": f"Postgres check failed: {str(e)}"},
        )