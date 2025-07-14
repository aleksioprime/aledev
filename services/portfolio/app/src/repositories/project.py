from abc import ABC, abstractmethod
from uuid import UUID
import logging

from sqlalchemy.exc import NoResultFound
from sqlalchemy import update, delete, select, func

from src.constants.base import LangEnum
from src.models.project import Project, ProjectTranslation
from src.repositories.base import BaseSQLRepository
from src.schemas.project import (
    ProjectQueryParams,
    ProjectCreateSchema,
    ProjectUpdateSchema,
    ProjectTranslationCreateSchema,
    ProjectTranslationUpdateSchema,
    )

logger = logging.getLogger(__name__)


class BaseProjectRepository(ABC):

    @abstractmethod
    async def get_by_id(self, project_id: UUID):
        ...

    @abstractmethod
    async def get_all(self, params: ProjectQueryParams):
        ...

    @abstractmethod
    async def create(self, body: ProjectCreateSchema):
        ...

    @abstractmethod
    async def update(self, project_id: UUID, body: ProjectUpdateSchema):
        ...

    @abstractmethod
    async def delete(self, project_id: UUID):
        ...


class ProjectRepository(BaseProjectRepository, BaseSQLRepository):

    async def get_by_id(self, project_id: UUID) -> Project | None:
        """
        Получает проект по его ID
        """
        stmt = select(Project).where(Project.id == project_id)
        result = await self.session.execute(stmt)
        return result.scalars().unique().one_or_none()

    async def get_all(self, params: ProjectQueryParams) -> tuple[list[Project], int]:
        """ Получает пагинированный список всех проектов и количество записей"""
        stmt = select(Project)
        count_stmt = select(func.count()).select_from(Project)

        if params.is_favorite is not None:
            stmt = stmt.where(Project.is_favorite == params.is_favorite)
            count_stmt = count_stmt.where(Project.is_favorite == params.is_favorite)

        stmt = stmt.limit(params.limit).offset(params.offset)

        result = await self.session.execute(stmt)
        projects = result.scalars().unique().all()

        total = (await self.session.execute(count_stmt)).scalar_one()
        return projects, total

    async def create(self, body: ProjectCreateSchema) -> Project:
        """ Создаёт новый проект """
        create_data = body.model_dump(exclude_unset=True, exclude={"translations"})

        project = Project(**create_data)
        project.translations = [
            ProjectTranslation(**tr.model_dump(exclude_unset=True))
            for tr in (body.translations or [])
        ]
        self.session.add(project)
        await self.session.flush()
        return project

    async def update(self, project_id: UUID, body: ProjectUpdateSchema) -> Project | None:
        """ Обновляет проект по его ID """
        update_data = {key: value for key, value in body.dict(exclude_unset=True).items() if key != "translations"}
        if not update_data:
            raise NoResultFound("Нет данных для обновления")

        stmt = (
            update(Project)
            .where(Project.id == project_id)
            .values(**update_data)
            .execution_options(synchronize_session="fetch")
        )

        await self.session.execute(stmt)

        if body.translations is not None:
            await self.session.execute(
                delete(ProjectTranslation).where(ProjectTranslation.project_id == project_id)
            )

            if body.translations:
                objects = [
                    ProjectTranslation(
                        project_id=project_id,
                        lang=tr.lang,
                        title=tr.title,
                        description=tr.description
                    )
                    for tr in body.translations
                ]
                self.session.add_all(objects)

        return await self.get_by_id(project_id)

    async def delete(self, project_id: UUID) -> None:
        """ Удаляет проект по его ID """
        project = await self.get_by_id(project_id)

        if project:
            await self.session.delete(project)

    async def add_translation(self, project_id: UUID, body: ProjectTranslationCreateSchema) -> ProjectTranslation:
        """ Добавляет новый перевод к проекту """
        create_data = body.model_dump(exclude_unset=True, exclude={"translations"})
        create_data["project_id"] = project_id

        translation = ProjectTranslation(**create_data)

        self.session.add(translation)
        await self.session.flush()

        return translation

    async def update_translation(self, project_id: UUID, lang: LangEnum, body: ProjectTranslationUpdateSchema) -> ProjectTranslation | None:
        """ Обновляет перевод проекта """

        stmt = (
            update(ProjectTranslation)
            .where(ProjectTranslation.project_id == project_id, ProjectTranslation.lang == lang)
            .values(**body.dict(exclude_unset=True))
            .execution_options(synchronize_session="fetch")
        )
        await self.session.execute(stmt)

        stmt = select(ProjectTranslation).where(ProjectTranslation.project_id == project_id, ProjectTranslation.lang == lang)
        result = await self.session.execute(stmt)

        return result.scalars().unique().one_or_none()

    async def delete_translation(self, project_id: UUID, lang: LangEnum) -> None:
        """ Удаляет перевод проекта """
        stmt = select(ProjectTranslation).where(ProjectTranslation.project_id == project_id, ProjectTranslation.lang == lang)
        translation = (await self.session.execute(stmt)).scalars().unique().one_or_none()

        if translation:
            await self.session.delete(translation)
            return True

        return False