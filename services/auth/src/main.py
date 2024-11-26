import logging
import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

from src.core.logger import LOGGING
from src.api.v1 import ping, auth
from src.exceptions.handlers import register_exception_handlers
from src.core.config import settings
from src.db import redis


@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Управление жизненным циклом приложения FastAPI
    """
    redis.redis = Redis(host=settings.redis.host, port=settings.redis.port)
    yield
    await redis.redis.close()


app = FastAPI(
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
)

# Регистрация обработчиков исключений
register_exception_handlers(app)

app.include_router(ping.router, prefix='/ping', tags=['Ping'])
app.include_router(auth.router, prefix='/api/v1', tags=['Auth'])
# app.include_router(user.router, prefix='/api/v1', tags=['User'])
# app.include_router(role.router, prefix='/api/v1', tags=['Role'])
# app.include_router(permission.router, prefix='/api/v1', tags=['Permission'])


if __name__ == '__main__':
    uvicorn.run(
        'main:app', host=settings.default_host, port=settings.default_port, log_config=LOGGING, log_level=logging.DEBUG, reload=True,
    )