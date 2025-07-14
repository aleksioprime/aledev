import logging
from uuid import UUID

from sqlalchemy.exc import NoResultFound, IntegrityError

from src.constants.base import LangEnum
from src.exceptions.base import BaseException, NotFoundException
from src.repositories.uow import UnitOfWork
from src.schemas.pagination import PaginatedResponse
from src.schemas.project import (
    ProjectQueryParams,
    ProjectSchema,
    ProjectCreateSchema,
    ProjectUpdateSchema,
    ProjectTranslationSchema,
    ProjectTranslationCreateSchema,
    ProjectTranslationUpdateSchema
    )

logger = logging.getLogger(__name__)


class ProjectService:

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_all(self, params: ProjectQueryParams) -> PaginatedResponse[ProjectSchema]:
        """
        Выдаёт пагинированную информацию обо всех проектах
        """
        async with self.uow:
            projects, total = await self.uow.project.get_all(params)

        items = [ProjectSchema.model_validate(project) for project in projects]

        return PaginatedResponse[ProjectSchema](
            items=items,
            total=total,
            limit=params.limit,
            offset=params.offset,
            has_next=(params.offset + 1) * params.limit < total,
            has_previous=params.offset > 0
        )

    async def get_by_id(self, project_id: UUID) -> ProjectSchema:
        """
        Выдаёт информацию о проекте по его ID
        """
        async with self.uow:
            project = await self.uow.project.get_by_id(project_id)

            if not project:
                raise NotFoundException(f"Проект с ID {project_id} не найден")

        return project

    async def create(self, body: ProjectCreateSchema) -> ProjectSchema:
        """
        Создаёт проект
        """
        async with self.uow:
            try:
                created_project = await self.uow.project.create(body)

            except IntegrityError as e:
                raise BaseException("Ошибка ограничения целостности данных в базе данных") from e

        return created_project

    async def update(self, project_id: UUID, body: ProjectUpdateSchema) -> ProjectSchema:
        """
        Обновляет информацию о проекте
        """
        async with self.uow:
            try:
                updated_project = await self.uow.project.update(project_id, body)
            except NoResultFound as e:
                raise BaseException("Нет данных для обновления") from e

            if not updated_project:
                raise NotFoundException(f"Проект с ID {project_id} не найден")

        return updated_project

    async def delete(self, project_id: UUID) -> None:
        """
        Удаляет проект
        """
        async with self.uow:
            project = await self.uow.project.get_by_id(project_id)

            if not project:
                raise NotFoundException(f"Проект с ID  {project_id} не найден")

            await self.uow.project.delete(project_id)

    async def add_translation(self, project_id: UUID, body: ProjectTranslationCreateSchema) -> ProjectTranslationSchema:
        """
        Добавляет перевод к проекту
        """
        async with self.uow:
            try:
                added_translation = await self.uow.project.add_translation(project_id, body)

            except IntegrityError as e:
                raise BaseException("Ошибка ограничения целостности данных в базе данных") from e

        return added_translation

    async def update_translation(self, project_id: UUID, lang: LangEnum, body: ProjectTranslationUpdateSchema) -> ProjectTranslationSchema:
        """
        Обновляет перевод у проекта
        """
        async with self.uow:
            updated_translation = await self.uow.project.update_translation(project_id, lang, body)

            if not updated_translation:
                raise NotFoundException(f"Перевод <{lang}> не найден")

        return updated_translation

    async def delete_translation(self, project_id: UUID, lang: LangEnum) -> None:
        """
        Удаляет перевод у проекта
        """
        async with self.uow:
            deleted = await self.uow.project.delete_translation(project_id, lang)

            if not deleted:
                raise NotFoundException(f"Перевод <{lang}> не найден")
