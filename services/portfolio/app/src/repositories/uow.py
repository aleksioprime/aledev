from src.db.postgres import async_session_maker

from src.repositories.project import ProjectRepository
from src.repositories.experience import ExperienceRepository
from src.repositories.feedback import FeedbackRepository
from src.repositories.achievement import AchievementRepository
from src.repositories.mentoring import MentoringRepository


class UnitOfWork:
    """
    Единица работы: одна сессия и транзакция на набор репозиториев
    """
    def __init__(self):
        self.session_factory = async_session_maker
        self.project = None
        self.experience = None
        self.feedback = None
        self.achievement = None
        self.mentoring = None

    async def __aenter__(self):
        self.session = self.session_factory()
        self.project = ProjectRepository(self.session)
        self.experience = ExperienceRepository(self.session)
        self.feedback = FeedbackRepository(self.session)
        self.achievement = AchievementRepository(self.session)
        self.mentoring = MentoringRepository(self.session)

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()
        await self.session.close()

    async def commit(self):
        """
        Фиксирует транзакцию
        """
        await self.session.commit()

    async def rollback(self):
        """
        Откатывает транзакцию
        """
        await self.session.rollback()