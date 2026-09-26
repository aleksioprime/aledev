import logging
from uuid import UUID

from sqlalchemy.exc import NoResultFound, IntegrityError

from src.constants.base import LangEnum
from src.exceptions.base import BaseException, NotFoundException
from src.repositories.uow import UnitOfWork
from src.schemas.pagination import PaginatedResponse
from src.schemas.experience import (
    ExperienceQueryParams,
    ExperienceSchema,
    ExperienceCreateSchema,
    ExperienceUpdateSchema,
    ExperienceTranslationSchema,
    ExperienceTranslationCreateSchema,
    ExperienceTranslationUpdateSchema
    )

logger = logging.getLogger(__name__)


class ExperienceService:

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_all(self, params: ExperienceQueryParams) -> PaginatedResponse[ExperienceSchema]:
        """
        Выдаёт пагинированную информацию обо всех записях опыта работы
        """
        async with self.uow:
            experiences, total = await self.uow.experience.get_all(params)

        items = [ExperienceSchema.model_validate(experience) for experience in experiences]

        return PaginatedResponse[ExperienceSchema](
            items=items,
            total=total,
            limit=params.limit,
            offset=params.offset,
            has_next=(params.offset + 1) * params.limit < total,
            has_previous=params.offset > 0
        )

    async def get_by_id(self, experience_id: UUID) -> ExperienceSchema:
        """
        Выдаёт информацию о записи опыта работы по её ID
        """
        async with self.uow:
            experience = await self.uow.experience.get_by_id(experience_id)

            if not experience:
                raise NotFoundException(f"Запись об опыте работы с ID {experience_id} не найдена")

        return experience

    async def create(self, body: ExperienceCreateSchema) -> ExperienceSchema:
        """
        Создаёт запись об опыте работы
        """
        async with self.uow:
            try:
                created_experience = await self.uow.experience.create(body)

            except IntegrityError as e:
                raise BaseException("Ошибка ограничения целостности данных в базе данных") from e

        return created_experience

    async def update(self, experience_id: UUID, body: ExperienceUpdateSchema) -> ExperienceSchema:
        """
        Обновляет запись об опыте работы
        """
        async with self.uow:
            try:
                updated_experience = await self.uow.experience.update(experience_id, body)
            except NoResultFound as e:
                raise BaseException("Нет данных для обновления") from e

            if not updated_experience:
                raise NotFoundException(f"Запись об опыте работы с ID {experience_id} не найдена")

        return updated_experience

    async def delete(self, experience_id: UUID) -> None:
        """
        Удаляет запись об опыте работы
        """
        async with self.uow:
            experience = await self.uow.experience.get_by_id(experience_id)

            if not experience:
                raise NotFoundException(f"Запись об опыте работы с ID  {experience_id} не найдена")

            await self.uow.experience.delete(experience_id)

    async def add_translation(self, experience_id: UUID, body: ExperienceTranslationCreateSchema) -> ExperienceTranslationSchema:
        """
        Добавляет перевод к записе об опыте работы
        """
        async with self.uow:
            try:
                added_translation = await self.uow.experience.add_translation(experience_id, body)

            except IntegrityError as e:
                raise BaseException("Ошибка ограничения целостности данных в базе данных") from e

        return added_translation

    async def update_translation(self, experience_id: UUID, lang: LangEnum, body: ExperienceTranslationUpdateSchema) -> ExperienceTranslationSchema:
        """
        Обновляет перевод у записи об опыте работы
        """
        async with self.uow:
            updated_translation = await self.uow.experience.update_translation(experience_id, lang, body)

            if not updated_translation:
                raise NotFoundException(f"Перевод <{lang}> не найден")

        return updated_translation

    async def delete_translation(self, experience_id: UUID, lang: LangEnum) -> None:
        """
        Удаляет перевод у записи об опыте работы
        """
        async with self.uow:
            deleted = await self.uow.experience.delete_translation(experience_id, lang)

            if not deleted:
                raise NotFoundException(f"Перевод <{lang}> не найден")
