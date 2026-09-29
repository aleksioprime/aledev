"""
Интеграционные тесты API портфолио.

Нужна пустая база PostgreSQL: параметры берутся из DB_HOST / DB_PORT / DB_USER / DB_PASSWORD / DB_NAME.
Перед тестами схема пересоздаётся миграциями (с начальными данными из init-миграции).
"""
import os
import subprocess
import sys
import time
import uuid
from pathlib import Path

import httpx
import jwt
import pytest

APP_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(APP_DIR))

# Внешние сервисы в тестах не используются
os.environ.setdefault("TURNSTILE_SECRET_KEY", "test")
os.environ.setdefault("SMTP_PASSWORD", "test")


def _alembic(*args: str) -> None:
    subprocess.run([sys.executable, "-m", "alembic", *args], cwd=APP_DIR, check=True, capture_output=True)


@pytest.fixture(scope="session", autouse=True)
def database():
    _alembic("downgrade", "base")
    _alembic("upgrade", "head")
    yield


@pytest.fixture(scope="session")
def app(database):
    from src.main import app as fastapi_app

    return fastapi_app


@pytest.fixture
async def client(app):
    # ASGITransport не запускает lifespan, поэтому фоновый воркер писем в тестах не стартует
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as c:
        yield c


@pytest.fixture(scope="session")
def admin_headers():
    from src.core.config import settings

    token = jwt.encode(
        {"sub": str(uuid.uuid4()), "is_superuser": True, "exp": int(time.time()) + 3600},
        settings.jwt.secret_key,
        algorithm=settings.jwt.algorithm,
    )
    return {"Authorization": f"Bearer {token}"}
