import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Enum as SqlEnum, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.constants.base import LangEnum
from src.db.postgres import Base


class MentoringPage(Base):
    __tablename__ = "mentoring_pages"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    slug: Mapped[str] = mapped_column(String(80), nullable=False, unique=True, default="mentoring")
    is_published: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    translations: Mapped[list["MentoringPageTranslation"]] = relationship(
        back_populates="page", cascade="all, delete-orphan", lazy="selectin"
    )
    metrics: Mapped[list["MentoringMetric"]] = relationship(
        back_populates="page", cascade="all, delete-orphan", lazy="selectin",
        order_by="MentoringMetric.order",
    )


class MentoringPageTranslation(Base):
    __tablename__ = "mentoring_page_translations"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    page_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mentoring_pages.id", ondelete="CASCADE"), index=True)
    lang: Mapped[LangEnum] = mapped_column(SqlEnum(LangEnum), nullable=False)
    kicker: Mapped[str] = mapped_column(String(255), nullable=False)
    title_start: Mapped[str] = mapped_column(String(255), nullable=False)
    title_accent: Mapped[str] = mapped_column(String(255), nullable=False)
    lead: Mapped[str] = mapped_column(Text, nullable=False)

    page: Mapped[MentoringPage] = relationship(back_populates="translations")

    __table_args__ = (UniqueConstraint("page_id", "lang", name="_mentoring_page_lang_uc"),)


class MentoringMetric(Base):
    __tablename__ = "mentoring_metrics"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    page_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mentoring_pages.id", ondelete="CASCADE"), index=True)
    key: Mapped[str] = mapped_column(String(40), nullable=False)
    value: Mapped[str] = mapped_column(String(40), nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    page: Mapped[MentoringPage] = relationship(back_populates="metrics")
    translations: Mapped[list["MentoringMetricTranslation"]] = relationship(
        back_populates="metric", cascade="all, delete-orphan", lazy="selectin"
    )

    __table_args__ = (UniqueConstraint("page_id", "key", name="_mentoring_metric_key_uc"),)


class MentoringMetricTranslation(Base):
    __tablename__ = "mentoring_metric_translations"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    metric_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mentoring_metrics.id", ondelete="CASCADE"), index=True)
    lang: Mapped[LangEnum] = mapped_column(SqlEnum(LangEnum), nullable=False)
    label: Mapped[str] = mapped_column(String(255), nullable=False)

    metric: Mapped[MentoringMetric] = relationship(back_populates="translations")

    __table_args__ = (UniqueConstraint("metric_id", "lang", name="_mentoring_metric_lang_uc"),)
