from redis.asyncio import Redis
from typing import Annotated, List, Callable
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.redis import get_redis
from src.db.postgres import get_db_session
from src.services.auth import AuthService
from src.repositories.auth import AuthRepository
from src.utils.token import JWTHelper



def get_jwt_helper() -> JWTHelper:
    return JWTHelper()


async def get_auth_repository(
        session: Annotated[AsyncSession, Depends(get_db_session)]
        ) -> AuthRepository:
    """
    Получает экземпляр AuthRepository с переданным AsyncSession (асинхронная сессия базы данных)
    """
    return AuthRepository(session)

async def get_auth_service(
        jwt_helper: Annotated[JWTHelper, Depends(get_jwt_helper)],
        repository: Annotated[AuthRepository, Depends(get_auth_repository)],
        redis: Annotated[Redis, Depends(get_redis)],
):
    """
    Получает экземпляр AuthService с переданными зависимостями
    """
    return AuthService(repository, redis, jwt_helper)