from uuid import UUID
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from src.models.user import User, LoginHistory
from src.models.role import Role
from src.exceptions.database import RecordNotFoundError, DatabaseException

class AuthRepository():
    """
    Репозиторий для работы с данными пользователей и их историей аутентификации
    """

    def __init__(self, session: AsyncSession):
        """
        Инициализация репозитория с объектом сессии базы данных
        """
        self.session = session

    async def get_user_by_login(self, login: str) -> Optional[User]:
        """
        Возвращает словарь пользователя или None, если пользователь не найден
        """
        query = select(User).filter_by(login=login)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        return user

    async def create_user(self, user: User) -> User:
        """
        Создает нового пользователя в базе данных
        """
        try:
            self.session.add(user)
            await self.session.flush()
            await self.session.commit()
            return user
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(f"Ошибка при создании пользователя: {str(e)}")

    async def get_user_roles(self, user_id: UUID) -> List[str]:
        """
        Получает список ролей пользователя по его ID
        """
        query = (
            select(Role.name)
            .join(Role.users)
            .filter(User.id == user_id)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def save_login_history(self, user_id: UUID, ip_address: str, user_agent: str):
        """
        Сохраняет запись об истории входа пользователя
        """
        try:
            history = LoginHistory(user_id=user_id, ip_address=ip_address, user_agent=user_agent)
            self.session.add(history)
            await self.session.flush()
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(f"Ошибка при сохранении истории входа: {str(e)}")