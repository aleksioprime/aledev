import uuid

from sqlalchemy import Column, DateTime, String, ForeignKey, func, Date
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from src.db.postgres import Base


class Participant(Base):
    __tablename__ = 'participant'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    phone = Column(String(15), nullable=True)
    date_of_birth = Column(Date, nullable=True)

    user = relationship("User", back_populates="participant", uselist=False)
    family_id = Column(UUID(as_uuid=True), ForeignKey('family.id'), nullable=False)
    family = relationship("Family", back_populates="participants")
    wishes = relationship("WishList", back_populates="participant", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f'<Participant {self.name}>'


class WishList(Base):
    __tablename__ = 'wish_list'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    description = Column(String(255), nullable=False)
    participant_id = Column(UUID(as_uuid=True), ForeignKey('participant.id'), nullable=False)

    participant = relationship("Participant", back_populates="wishes")

    def __repr__(self) -> str:
        return f'<WishList {self.description[:20]}>'


class User(Base):
    __tablename__ = 'user'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)

    participant = relationship("Participant", back_populates="user", uselist=False)

    def __repr__(self) -> str:
        return f'<User {self.email}>'
