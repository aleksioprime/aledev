import uvicorn
import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles

from src.core.config import settings
from src.core.logger import LOGGING
from src.api.v1 import router
from src.exceptions.handlers import register_exception_handlers

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Управление жизненным циклом приложения FastAPI.
    """
    yield


# Инициализация FastAPI-приложения
app = FastAPI(
    lifespan=lifespan, # Указание жизненного цикла приложения
    version="0.0.1", # Версия приложения
    title=settings.project_name, # Название приложения
    description=settings.project_description, # Описание приложения
    docs_url="/api", # URL для документации Swagger
    openapi_url="/api/openapi.json", # URL для OpenAPI схемы
    default_response_class=ORJSONResponse, # Быстрая обработка JSON с ORJSON
)

# Регистрация обработчиков исключений
register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)

os.makedirs(settings.media.base, exist_ok=True)
app.mount("/media", StaticFiles(directory=os.path.abspath(settings.media.base)), name="media")

# Подключение роутера для версии v1
app.include_router(router, prefix="/api/v1")

# Точка входа в приложение
if __name__ == "__main__":
    # Запуск Uvicorn-сервера
    uvicorn.run(
        "main:app",  # Указание приложения (main.py:app)
        host=settings.default_host,  # Хост из настроек
        port=settings.default_port,  # Порт из настроек
        log_config=LOGGING,  # Конфигурация логирования
        log_level=logging.INFO,  # Уровень логирования
        reload=True,  # Автоматическая перезагрузка при изменении файлов
    )