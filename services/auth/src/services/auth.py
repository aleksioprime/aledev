
import logging
from redis.asyncio import Redis
from fastapi import HTTPException

from src.models.user import User
from src.schemas.auth import RegisterSchema
from src.schemas.token import TokenSchema
from src.repositories.auth import AuthRepository
from src.utils.token import JWTHelper


class AuthService:
    """
    Сервис для управления аутентификацией, регистрацией и выходом пользователей
    """

    def __init__(self, repository: AuthRepository, redis: Redis, jwt_helper: JWTHelper):
        self.repository = repository
        self.redis = redis
        self.jwt_helper = jwt_helper

    async def register(self, body: RegisterSchema, ip_address: str, user_agent: str) -> TokenSchema:
        """
        Регистрирует нового пользователя и генерирует токены
        """
        existing_user = await self.repository.get_user_by_login(body.login)
        if existing_user:
            raise HTTPException(status_code=400, detail="Пользователь с таким логином уже существует")

        user = User(
            login=body.login,
            password=body.password,
            first_name=body.first_name,
            last_name=body.last_name,
        )
        logging.info(f"Пользователь для записи: {user}")
        await self.repository.create_user(user)

        roles = await self.repository.get_user_roles(user.id)
        access_token, refresh_token = self.jwt_helper.generate_token_pair(user.id, roles)

        await self.redis.set(f"refresh_token:{refresh_token}", str(user.id), ex=604800)

        await self.repository.save_login_history(user.id, ip_address, user_agent)

        return TokenSchema(access_token=access_token, refresh_token=refresh_token)

    async def login(self, login: str, password: str, ip_address: str, user_agent: str) -> TokenSchema:
        """
        Аутентифицирует пользователя и генерирует JWT токены
        """
        user = await self.repository.get_user_by_login(login)
        if not user or not user.check_password(password):
            raise HTTPException(status_code=400, detail="Неверный логин или пароль")

        roles = await self.repository.get_user_roles(user.id)
        access_token, refresh_token = self.jwt_helper.generate_token_pair(user.id, roles)

        await self.redis.set(f"refresh_token:{refresh_token}", str(user.id), ex=604800)

        await self.repository.save_login_history(user.id, ip_address, user_agent)

        return TokenSchema(access_token=access_token, refresh_token=refresh_token)

    async def logout(self, access_token: str, refresh_token: str):
        """
        Инвалидирует токены пользователя
        """
        await self.redis.set(f"revoked_token:{access_token}", "revoked", ex=3600)
        await self.redis.delete(f"refresh_token:{refresh_token}")

    async def refresh(self, refresh_token: str) -> TokenSchema:
        """
        Обновляет токен доступа, используя refresh токен
        """
        payload = self.jwt_helper.verify(refresh_token)
        user_id = payload["sub"]
        roles = payload["role"]

        stored_token = await self.redis.get(f"refresh_token:{refresh_token}")
        if not stored_token:
            raise HTTPException(status_code=400, detail="Недействительный токен обновления")

        access_token, new_refresh_token = self.jwt_helper.generate_token_pair(user_id, roles)

        await self.redis.set(f"refresh_token:{new_refresh_token}", user_id, ex=604800)
        await self.redis.delete(f"refresh_token:{refresh_token}")

        return TokenSchema(access_token=access_token, refresh_token=new_refresh_token)