from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.exceptions.auth import AuthException
from src.exceptions.database import DatabaseException

def register_exception_handlers(app: FastAPI):
    """
    Регистрирует обработчики исключений в приложении FastAPI
    """

    @app.exception_handler(AuthException)
    async def auth_exception_handler(request: Request, exc: AuthException):
        return JSONResponse(
            status_code=400,
            content={"detail": exc.message},
        )

    @app.exception_handler(DatabaseException)
    async def database_exception_handler(request: Request, exc: DatabaseException):
        return JSONResponse(
            status_code=500,
            content={"detail": exc.message},
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "detail": str(exc),
                "path": str(request.url),
            },
        )