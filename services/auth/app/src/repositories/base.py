from sqlalchemy.ext.asyncio import AsyncSession


class BaseSQLRepository:
    """
    Базовый репозиторий с сессией БД
    """

    def __init__(self, session: AsyncSession):
        self.session = session