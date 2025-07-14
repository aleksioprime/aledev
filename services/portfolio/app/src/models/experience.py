import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    DateTime,
    Date,
    Text,
    String,
    Boolean,
    ForeignKey,
    UniqueConstraint,
    Enum as SqlEnum,
)

from src.constants.base import LangEnum
from src.db.postgres import Base


class Experience(Base):
    """
    Модель опыта (работа, стажировка)
    """
    __tablename__ = "experiences"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    start_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    end_date: Mapped[datetime | None] = mapped_column(Date)
    is_current: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    translations: Mapped[list["ExperienceTranslation"]] = relationship(
        "ExperienceTranslation", back_populates="experience", cascade="all, delete-orphan", lazy="joined"
    )

    def __repr__(self) -> str:
        return f"<Experience {self.id}>"

class ExperienceTranslation(Base):
    """
    Модель перевода для опыта
    """
    __tablename__ = "experience_translations"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    experience_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("experiences.id"), index=True)
    lang: Mapped[LangEnum] = mapped_column(SqlEnum(LangEnum), nullable=False)
    position: Mapped[str] = mapped_column(String(255), nullable=False)
    company: Mapped[str] = mapped_column(String(255), nullable=False)
    responsibilities: Mapped[str | None] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)

    experience: Mapped["Experience"] = relationship(
        "Experience", back_populates="translations"
    )

    __table_args__ = (
        UniqueConstraint("experience_id", "lang", name="_experience_lang_uc"),
    )

    def __repr__(self) -> str:
        return f"<ExperienceTranslation lang={self.lang} experience_id={self.experience_id}>"