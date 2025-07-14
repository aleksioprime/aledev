from abc import ABC, abstractmethod
from uuid import UUID
import logging

from sqlalchemy.exc import NoResultFound
from sqlalchemy import update, select, func

from src.constants.base import LangEnum
from src.models.experience import Experience, ExperienceTranslation
from src.repositories.base import BaseSQLRepository
from src.schemas.experience import (
    ExperienceQueryParams,
    ExperienceCreateSchema,
    ExperienceUpdateSchema,
    ExperienceTranslationCreateSchema,
    ExperienceTranslationUpdateSchema,
    )

logger = logging.getLogger(__name__)


class BaseExperienceRepository(ABC):

    @abstractmethod
    async def get_by_id(self, experience_id: UUID):
        ...

    @abstractmethod
    async def get_all(self, params: ExperienceQueryParams):
        ...

    @abstractmethod
    async def create(self, body: ExperienceCreateSchema):
        ...

    @abstractmethod
    async def update(self, experience_id: UUID, body: ExperienceUpdateSchema):
        ...

    @abstractmethod
    async def delete(self, experience_id: UUID):
        ...


class ExperienceRepository(BaseExperienceRepository, BaseSQLRepository):

    async def get_by_id(self, experience_id: UUID) -> Experience | None:
        """
        Получает запись об опыте работы по её ID
        """
        stmt = select(Experience).where(Experience.id == experience_id)
        result = await self.session.execute(stmt)
        return result.scalars().unique().one_or_none()

    async def get_all(self, params: ExperienceQueryParams) -> tuple[list[Experience], int]:
        """ Получает пагинированный список всех записей об опыте работы и количество записей"""
        stmt = (
            select(Experience)
            .limit(params.limit)
            .offset(params.offset)
        )
        result = await self.session.execute(stmt)
        experiences = result.scalars().unique().all()

        count_stmt = select(func.count()).select_from(Experience)
        total = (await self.session.execute(count_stmt)).scalar_one()
        return experiences, total

    async def create(self, body: ExperienceCreateSchema) -> Experience:
        """ Создаёт новую запись об опыте работы """
        create_data = body.model_dump(exclude_unset=True, exclude={"translations"})

        experience = Experience(**create_data)
        experience.translations = [
            ExperienceTranslation(**tr.model_dump(exclude_unset=True))
            for tr in (body.translations or [])
        ]
        self.session.add(experience)
        await self.session.flush()
        return experience

    async def update(self, experience_id: UUID, body: ExperienceUpdateSchema) -> Experience | None:
        """ Обновляет запись об опыте работы по её ID """
        update_data = {key: value for key, value in body.dict(exclude_unset=True).items()}
        if not update_data:
            raise NoResultFound("Нет данных для обновления")

        stmt = (
            update(Experience)
            .where(Experience.id == experience_id)
            .values(**update_data)
            .execution_options(synchronize_session="fetch")
        )

        await self.session.execute(stmt)
        return await self.get_by_id(experience_id)

    async def delete(self, experience_id: UUID) -> None:
        """ Удаляет запись об опыте работы по её ID """
        experience = await self.get_by_id(experience_id)

        if experience:
            await self.session.delete(experience)

    async def add_translation(self, experience_id: UUID, body: ExperienceTranslationCreateSchema) -> ExperienceTranslation:
        """ Добавляет новый перевод к записи об опыте работы """
        create_data = body.model_dump(exclude_unset=True, exclude={"translations"})
        create_data["experience_id"] = experience_id

        translation = ExperienceTranslation(**create_data)

        self.session.add(translation)
        await self.session.flush()

        return translation

    async def update_translation(self, experience_id: UUID, lang: LangEnum, body: ExperienceTranslationUpdateSchema) -> ExperienceTranslation | None:
        """ Обновляет перевод к записи об опыте работы """

        stmt = (
            update(ExperienceTranslation)
            .where(ExperienceTranslation.experience_id == experience_id, ExperienceTranslation.lang == lang)
            .values(**body.dict(exclude_unset=True))
            .execution_options(synchronize_session="fetch")
        )
        await self.session.execute(stmt)

        stmt = select(ExperienceTranslation).where(ExperienceTranslation.experience_id == experience_id, ExperienceTranslation.lang == lang)
        result = await self.session.execute(stmt)

        return result.scalars().unique().one_or_none()

    async def delete_translation(self, experience_id: UUID, lang: LangEnum) -> None:
        """ Удаляет перевод к записи об опыте работы """
        stmt = select(ExperienceTranslation).where(ExperienceTranslation.experience_id == experience_id, ExperienceTranslation.lang == lang)
        translation = (await self.session.execute(stmt)).scalars().unique().one_or_none()

        if translation:
            await self.session.delete(translation)
            return True

        return False