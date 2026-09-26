from src.db.postgres import async_session_maker

from src.repositories.project import ProjectRepository
from src.repositories.experience import ExperienceRepository


class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session_maker
        self.project = None
        self.experience = None

    async def __aenter__(self):
        self.session = self.session_factory()
        self.project = ProjectRepository(self.session)
        self.experience = ExperienceRepository(self.session)

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()