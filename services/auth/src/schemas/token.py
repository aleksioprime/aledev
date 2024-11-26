from uuid import UUID

from pydantic import BaseModel


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class RefreshTokenCreate(BaseModel):
    user_id: UUID
    token: str


class RefreshTokenUpdate(BaseModel):
    old_token: str
    new_token: str


class RefreshTokenSchema(BaseModel):
    refresh_token: str