import uuid

from sqlalchemy import Column, DateTime, Text, String, Boolean, func
from sqlalchemy.dialects.postgresql import UUID


from src.db.postgres import Base


class Experience(Base):
    """
    Модель опыта (работа, стажировка)
    """
    __tablename__ = 'experiences'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    position = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=True)
    is_current = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime(timezone=True), default=func.now())

    def __repr__(self) -> str:
        return f'<Experience {self.position} at {self.company}>'