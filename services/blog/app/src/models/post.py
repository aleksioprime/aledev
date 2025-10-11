from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    Text,
    Integer,
    Index,
    Table,
    Column,
    ForeignKey,
    UniqueConstraint,
    Uuid,
)

from src.db.postgres import Base


# M2M таблица тегов
post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", Uuid(as_uuid=True), ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
    Index("ix_post_tags_post_id", "post_id"),
    Index("ix_post_tags_tag_id", "tag_id"),
)


class Category(Base):
    """
    Модель категории поста
    """
    __tablename__ = 'categories'

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(80), nullable=False, unique=True, index=True)
    slug: Mapped[str] = mapped_column(String(120), nullable=False, unique=True, index=True)

    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("categories.id", ondelete="SET NULL")
    )
    parent: Mapped[Category | None] = relationship(
        remote_side="Category.id", backref="children", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f'<Category {self.name}>'


class Tag(Base):
    """
    Модель тэгов поста
    """
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(String(80), nullable=False, unique=True, index=True)

    __table_args__ = (UniqueConstraint("name", name="uq_tag_name"),)

    def __repr__(self) -> str:
        return f'<Tag {self.name}>'


class Post(Base):
    """
    Модель постов
    """
    __tablename__ = 'posts'

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0, index=True)

    title: Mapped[str] = mapped_column(String(300), nullable=False)
    slug:  Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)

    excerpt: Mapped[str | None] = mapped_column(String(500))
    content_html: Mapped[str] = mapped_column(Text, nullable=False)
    cover_url: Mapped[str | None] = mapped_column(String(500))

    published: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        index=True,
    )

    category_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("categories.id", ondelete="SET NULL")
    )
    category: Mapped[Category | None] = relationship(lazy="selectin")

    tags: Mapped[list[Tag]] = relationship(
        secondary=post_tags, backref="posts", lazy="selectin", cascade="save-update"
    )

    def __repr__(self) -> str:
        return f'<Post {self.title}>'
