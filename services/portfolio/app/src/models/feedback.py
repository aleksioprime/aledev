import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, Integer, String, Text, Index, Enum as SqlEnum

from src.constants.base import FeedbackKind, FeedbackStatus, EmailStatus
from src.db.postgres import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _enum(enum_cls):
    # Храним как строки (без нативного типа PostgreSQL) - проще добавлять значения
    return SqlEnum(enum_cls, native_enum=False, length=20, values_callable=lambda e: [i.value for i in e])


class Feedback(Base):
    """
    Обращение с формы обратной связи (заказ или вопрос)
    """
    __tablename__ = "feedback_messages"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    kind: Mapped[FeedbackKind] = mapped_column(_enum(FeedbackKind), nullable=False, default=FeedbackKind.question)

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    contact: Mapped[str | None] = mapped_column(String(255))
    service: Mapped[str | None] = mapped_column(String(30))
    budget: Mapped[str | None] = mapped_column(String(30))
    deadline: Mapped[str | None] = mapped_column(String(100))
    message: Mapped[str] = mapped_column(Text, nullable=False)
    lang: Mapped[str | None] = mapped_column(String(5))

    status: Mapped[FeedbackStatus] = mapped_column(_enum(FeedbackStatus), nullable=False, default=FeedbackStatus.new)
    admin_note: Mapped[str | None] = mapped_column(Text)

    email_status: Mapped[EmailStatus] = mapped_column(_enum(EmailStatus), nullable=False, default=EmailStatus.pending)
    email_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    email_provider: Mapped[str | None] = mapped_column(String(20))
    email_error: Mapped[str | None] = mapped_column(Text)
    emailed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    ip: Mapped[str | None] = mapped_column(String(64))
    user_agent: Mapped[str | None] = mapped_column(String(512))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow, onupdate=_utcnow, nullable=False)

    __table_args__ = (
        Index("ix_feedback_messages_created_at", "created_at"),
        Index("ix_feedback_messages_status", "status"),
        Index("ix_feedback_messages_email_status", "email_status"),
    )

    def __repr__(self) -> str:
        return f"<Feedback {self.id} {self.kind}>"
