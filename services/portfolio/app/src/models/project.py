import uuid

from sqlalchemy import Column, DateTime, Text, String, Boolean, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


from src.db.postgres import Base


class Project(Base):
    """
    Модель проекта для портфолио
    """
    __tablename__ = 'projects'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    title = Column(String(255), nullable=False, index=True)
    stack = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    link = Column(String(255), nullable=True)
    github_url = Column(String(255), nullable=True)
    demo_url = Column(String(255), nullable=True)
    is_favorite = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    article = relationship('Article', back_populates='project', uselist=False)

    def __repr__(self) -> str:
        return f'<Project {self.title}>'


class Article(Base):
    """
    Модель статьи
    """
    __tablename__ = 'articles'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey('projects.id'), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    content = Column(Text, nullable=True)
    is_public = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    project = relationship('Project', back_populates='article', uselist=False)

    def __repr__(self):
        return f'<Article {self.title}>'


class ArticleTOC(Base):
    """
    Модель оглавления
    """
    __tablename__ = 'article_tocs'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    article_id = Column(UUID(as_uuid=True), ForeignKey('articles.id'), nullable=False, index=True)
    parent_id = Column(UUID(as_uuid=True), ForeignKey('article_tocs.id'), nullable=True, index=True)
    title = Column(String(255), nullable=False)
    anchor = Column(String(255), nullable=True)
    order = Column(String(10), nullable=True)

    def __repr__(self):
        return f'<ArticleTOC {self.title}>'