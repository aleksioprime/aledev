import uuid

from sqlalchemy import Column, DateTime, String, ForeignKey, Table, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import check_password_hash, generate_password_hash

from src.db.postgres import Base


user_roles = Table('user_roles', Base.metadata,
                   Column('user_id', UUID(as_uuid=True), ForeignKey('user.id', ondelete="CASCADE")),
                   Column('role_id', UUID(as_uuid=True), ForeignKey('role.id', ondelete="CASCADE"))
                   )


class User(Base):
    __tablename__ = 'user'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    login = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    created_at = Column(DateTime(timezone=True), default=func.now())

    roles = relationship("Role", secondary=user_roles, back_populates="users")
    login_history = relationship("LoginHistory", back_populates="user", cascade="all, delete-orphan")

    def __init__(self, login: str, password: str, first_name: str, last_name: str) -> None:
        self.login = login
        self.password = generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def __repr__(self) -> str:
        return f'<User {self.login}>'


class LoginHistory(Base):
    __tablename__ = "loginhistory"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id', ondelete="CASCADE"), index=True)
    ip_address = Column(String(255), nullable=False)
    user_agent = Column(String(255), nullable=False)
    login_at = Column(DateTime(timezone=True), default=func.now())

    user = relationship("User", back_populates="login_history")