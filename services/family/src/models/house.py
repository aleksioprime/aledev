import uuid

from sqlalchemy import Column, String, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from src.db.postgres import Base


class House(Base):
    __tablename__ = 'house'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    type = Column(String(255), index=True, nullable=False)
    area = Column(String(50), nullable=True)
    address = Column(String(255), nullable=True)

    family_id = Column(UUID(as_uuid=True), ForeignKey('family.id'), nullable=False)
    family = relationship("Family", back_populates="houses")

    def __repr__(self) -> str:
        return f'<House {self.name}, Type: {self.type}>'