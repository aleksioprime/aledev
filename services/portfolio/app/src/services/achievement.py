from uuid import UUID

from src.exceptions.base import NotFoundException
from src.repositories.uow import UnitOfWork
from src.schemas.achievement import AchievementCreateSchema, AchievementQueryParams, AchievementSchema, AchievementUpdateSchema
from src.schemas.pagination import PaginatedResponse


class AchievementService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_all(
        self,
        params: AchievementQueryParams,
        *,
        include_unpublished: bool = False,
    ) -> PaginatedResponse[AchievementSchema]:
        async with self.uow:
            items, total = await self.uow.achievement.get_all(
                params,
                include_unpublished=include_unpublished,
            )
        return PaginatedResponse[AchievementSchema](
            items=[AchievementSchema.model_validate(item) for item in items],
            total=total,
            limit=params.limit,
            offset=params.offset,
            has_next=params.offset + params.limit < total,
            has_previous=params.offset > 0,
        )

    async def get_by_id(self, achievement_id: UUID) -> AchievementSchema:
        async with self.uow:
            achievement = await self.uow.achievement.get_by_id(achievement_id)
            if not achievement:
                raise NotFoundException(f"Достижение с ID {achievement_id} не найдено")
        return AchievementSchema.model_validate(achievement)

    async def create(self, body: AchievementCreateSchema) -> AchievementSchema:
        async with self.uow:
            achievement = await self.uow.achievement.create(body)
        return AchievementSchema.model_validate(achievement)

    async def update(self, achievement_id: UUID, body: AchievementUpdateSchema) -> AchievementSchema:
        async with self.uow:
            achievement = await self.uow.achievement.update(achievement_id, body)
            if not achievement:
                raise NotFoundException(f"Достижение с ID {achievement_id} не найдено")
        return AchievementSchema.model_validate(achievement)

    async def delete(self, achievement_id: UUID) -> None:
        async with self.uow:
            if not await self.uow.achievement.delete(achievement_id):
                raise NotFoundException(f"Достижение с ID {achievement_id} не найдено")
