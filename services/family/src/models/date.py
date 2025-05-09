import uuid

from sqlalchemy import Column, DateTime, String, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from src.db.postgres import Base


class ImportantDate(Base):
    __tablename__ = 'important_date'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    family_id = Column(UUID(as_uuid=True), ForeignKey('family.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(255), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    type = Column(String(50), nullable=True)

    family = relationship("Family", back_populates="important_dates")

    def __repr__(self) -> str:
        return f'<ImportantDate {self.name} ({self.date})>'