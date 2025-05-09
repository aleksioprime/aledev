import uuid

from sqlalchemy import Column, DateTime, String, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from src.db.postgres import Base


class Family(Base):
    __tablename__ = 'family'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(255), unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)

    important_dates = relationship("ImportantDate", back_populates="family", cascade="all, delete-orphan")
    houses = relationship("House", back_populates="family", cascade="all, delete-orphan")
    participants = relationship("Participant", back_populates="family", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="family", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f'<Family {self.name}>'