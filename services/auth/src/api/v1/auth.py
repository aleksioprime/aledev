import logging

from fastapi import APIRouter, Depends, HTTPException, status, Body, Request

from src.dependencies.auth import get_auth_service
from src.exceptions.auth import RegisterError, AuthException
from src.schemas.auth import AuthSchema, RegisterSchema
from src.schemas.token import TokenSchema, RefreshTokenSchema
from src.services.auth import AuthService

router = APIRouter()


@router.post(
        path="/register",
        summary="Регистрация нового пользователя",
        description="Создает нового пользователя в системе и возвращает токены доступа и обновления",
        status_code=status.HTTP_201_CREATED,
        response_model=TokenSchema,
        )
async def register(
    request: Request,
    user: RegisterSchema,
    service: AuthService = Depends(get_auth_service)
    ) -> TokenSchema:
    logging.debug(f"Registering user: {user.login}")
    try:
        ip_address = request.client.host
        user_agent = request.headers.get("user-agent", "")
        tokens: TokenSchema = await service.register(user, ip_address, user_agent)
    except RegisterError as e:
        logging.info(f"Register error: {e.message}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    return tokens


@router.post(
        path="/login",
        summary="Вход пользователя в систему",
        description="Аутентифицирует пользователя и возвращает токены доступа и обновления",
        response_model=TokenSchema,
        )
async def login(
    request: Request,
    user: AuthSchema,
    service: AuthService = Depends(get_auth_service),
    ):
    try:
        ip_address = request.client.host
        user_agent = request.headers.get("user-agent", "")
        user = await service.login(user.login, user.password, ip_address, user_agent)
    except AuthException as e:
        logging.error(f"Login failed: {e.message}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

    return user


@router.post(
        path="/logout",
        summary="Выход пользователя из системы",
        description="Инвалидирует текущий токен доступа пользователя",
        )
async def logout(
    tokens: TokenSchema,
    service: AuthService = Depends(get_auth_service),
    ):
    """
    Выход из системы: инвалидирует токены
    """
    try:
        await service.logout(tokens.access_token, tokens.refresh_token)
    except AuthException as e:
        logging.error(f"Logout error: {e.message}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)


@router.post(
        path='/refresh',
        response_model=TokenSchema,
        summary="Обновление токена доступа",
        description="Создает новый токен доступа на основе действительного токена обновления")
async def refresh_token(
    token: RefreshTokenSchema,
    service: AuthService = Depends(get_auth_service),
    )-> TokenSchema:
    """
    Обновление токена доступа.
    """
    try:
        tokens = await service.refresh(token.refresh_token)
        return tokens
    except AuthException as e:
        logging.error(f"Token refresh failed: {e.message}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)