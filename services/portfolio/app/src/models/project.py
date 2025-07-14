import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    Text,
    ForeignKey,
    UniqueConstraint,
    Enum as SqlEnum,
)

from src.constants.base import LangEnum
from src.db.postgres import Base


class Project(Base):
    """
    Модель проекта для портфолио
    """
    __tablename__ = 'projects'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    stack: Mapped[str | None] = mapped_column(String(255))
    link: Mapped[str | None] = mapped_column(String(255))
    github_url: Mapped[str | None] = mapped_column(String(255))
    demo_url: Mapped[str | None] = mapped_column(String(255))
    is_favorite: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    article: Mapped["Article | None"] = relationship(
        "Article", back_populates="project", uselist=False
    )

    translations: Mapped[list["ProjectTranslation"]] = relationship(
        "ProjectTranslation", back_populates="project", cascade="all, delete-orphan", lazy="joined"
    )

    def __repr__(self) -> str:
        return f'<Project {self.title}>'


class ProjectTranslation(Base):
    """
    Модель перевода для проекта
    """
    __tablename__ = 'project_translations'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"), index=True)
    lang: Mapped[LangEnum] = mapped_column(SqlEnum(LangEnum), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)

    project: Mapped["Project"] = relationship(
        "Project", back_populates="translations"
    )

    __table_args__ = (
        UniqueConstraint("project_id", "lang", name="_project_lang_uc"),
    )

    def __repr__(self) -> str:
        return f'<ProjectTranslation lang={self.lang} project_id={self.project_id}>'


class Article(Base):
    """
    Модель статьи
    """
    __tablename__ = 'articles'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    content: Mapped[str | None] = mapped_column(Text)
    is_public: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    project: Mapped["Project"] = relationship(
        "Project", back_populates="article", uselist=False
    )

    def __repr__(self):
        return f'<Article {self.title}>'


class ArticleTOC(Base):
    """
    Модель оглавления
    """
    __tablename__ = 'article_tocs'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    article_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("articles.id"), index=True)
    parent_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("article_tocs.id"), index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    anchor: Mapped[str | None] = mapped_column(String(255))
    order: Mapped[str | None] = mapped_column(String(10))

    def __repr__(self):
        return f'<ArticleTOC {self.title}>'