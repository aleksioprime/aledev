from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models.mentoring import (
    MentoringMetric,
    MentoringMetricTranslation,
    MentoringPage,
    MentoringPageTranslation,
)
from src.repositories.base import BaseSQLRepository
from src.schemas.mentoring import MentoringPageUpdateSchema


class MentoringRepository(BaseSQLRepository):
    """
    Репозиторий секции наставничества
    """
    async def get_page(self, *, include_unpublished: bool = False) -> MentoringPage | None:
        """
        Получает контент секции с переводами и цифрами
        """
        stmt = (
            select(MentoringPage)
            .where(MentoringPage.slug == "mentoring")
            .options(
                selectinload(MentoringPage.translations),
                selectinload(MentoringPage.metrics).selectinload(MentoringMetric.translations),
            )
        )
        if not include_unpublished:
            stmt = stmt.where(MentoringPage.is_published.is_(True))
        result = await self.session.execute(stmt)
        return result.scalars().unique().one_or_none()

    async def update_page(self, body: MentoringPageUpdateSchema) -> MentoringPage:
        """
        Заменяет тексты и цифры секции
        """
        page = await self.get_page(include_unpublished=True)
        if page is None:
            raise LookupError("Блок наставничества не найден")

        page.is_published = body.is_published
        # Удаляем старые строки до вставки новых, иначе конфликт уникальных ключей
        page.translations.clear()
        page.metrics.clear()
        await self.session.flush()

        page.translations = [
            MentoringPageTranslation(**translation.model_dump())
            for translation in body.translations
        ]
        page.metrics = [
            MentoringMetric(
                **metric.model_dump(exclude={"translations"}),
                translations=[
                    MentoringMetricTranslation(**translation.model_dump())
                    for translation in metric.translations
                ],
            )
            for metric in body.metrics
        ]
        await self.session.flush()
        return await self.get_page(include_unpublished=True)
