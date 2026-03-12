from src.db.postgres import async_session_maker

from src.repositories.post import PostRepository
from src.repositories.category import CategoryRepository
from src.repositories.tag import TagRepository


class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session_maker
        self.post = None
        self.category = None
        self.tag = None

    async def __aenter__(self):
        self.session = self.session_factory()
        self.post = PostRepository(self.session)
        self.category = CategoryRepository(self.session)
        self.tag = TagRepository(self.session)

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