from src.exceptions.base import NotFoundException
from src.repositories.uow import UnitOfWork
from src.schemas.mentoring import MentoringPageSchema, MentoringPageUpdateSchema


class MentoringService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_page(self, *, include_unpublished: bool = False) -> MentoringPageSchema:
        async with self.uow:
            page = await self.uow.mentoring.get_page(include_unpublished=include_unpublished)
            if page is None:
                raise NotFoundException("Контент блока наставничества не найден")
        return MentoringPageSchema.model_validate(page)

    async def update_page(self, body: MentoringPageUpdateSchema) -> MentoringPageSchema:
        async with self.uow:
            page = await self.uow.mentoring.update_page(body)
        return MentoringPageSchema.model_validate(page)
