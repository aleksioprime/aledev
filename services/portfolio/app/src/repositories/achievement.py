from uuid import UUID

from sqlalchemy import delete, func, select, update

from src.models.achievement import Achievement, AchievementTranslation
from src.repositories.base import BaseSQLRepository
from src.schemas.achievement import AchievementCreateSchema, AchievementQueryParams, AchievementUpdateSchema


class AchievementRepository(BaseSQLRepository):
    """
    Репозиторий достижений
    """
    async def get_by_id(self, achievement_id: UUID) -> Achievement | None:
        """
        Получает достижение по ID
        """
        result = await self.session.execute(select(Achievement).where(Achievement.id == achievement_id))
        return result.scalars().unique().one_or_none()

    async def get_all(
        self,
        params: AchievementQueryParams,
        *,
        include_unpublished: bool = False,
    ) -> tuple[list[Achievement], int]:
        """
        Получает страницу достижений и их общее количество
        """
        conditions = []
        if not include_unpublished:
            conditions.append(Achievement.is_published.is_(True))
        if params.category:
            conditions.append(Achievement.category == params.category)
        if params.scope:
            conditions.append(Achievement.scope == params.scope)

        stmt = (
            select(Achievement)
            .where(*conditions)
            .order_by(Achievement.is_featured.desc(), Achievement.year.desc().nullslast(), Achievement.order, Achievement.created_at.desc())
            .limit(params.limit)
            .offset(params.offset)
        )
        items = (await self.session.execute(stmt)).scalars().unique().all()
        total = (await self.session.execute(
            select(func.count()).select_from(Achievement).where(*conditions)
        )).scalar_one()
        return list(items), total

    async def create(self, body: AchievementCreateSchema) -> Achievement:
        """
        Создаёт достижение с переводами
        """
        data = body.model_dump(exclude={"translations"})
        achievement = Achievement(**data)
        achievement.translations = [
            AchievementTranslation(**translation.model_dump())
            for translation in body.translations
        ]
        self.session.add(achievement)
        await self.session.flush()
        return achievement

    async def update(self, achievement_id: UUID, body: AchievementUpdateSchema) -> Achievement | None:
        """
        Обновляет достижение и заменяет переводы
        """
        achievement = await self.get_by_id(achievement_id)
        if not achievement:
            return None

        data = body.model_dump(exclude_unset=True, exclude={"translations"})
        if data:
            await self.session.execute(
                update(Achievement)
                .where(Achievement.id == achievement_id)
                .values(**data)
                .execution_options(synchronize_session="fetch")
            )

        if body.translations is not None:
            await self.session.execute(
                delete(AchievementTranslation).where(AchievementTranslation.achievement_id == achievement_id)
            )
            self.session.add_all([
                AchievementTranslation(
                    achievement_id=achievement_id,
                    **translation.model_dump(),
                )
                for translation in body.translations
            ])

        await self.session.flush()
        # Перечитываем запись после массовых UPDATE/DELETE
        await self.session.refresh(achievement)
        return achievement

    async def delete(self, achievement_id: UUID) -> bool:
        """
        Удаляет достижение
        """
        achievement = await self.get_by_id(achievement_id)
        if not achievement:
            return False
        await self.session.delete(achievement)
        return True
