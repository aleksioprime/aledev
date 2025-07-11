from fastapi import Depends, HTTPException, status

from src.schemas.security import UserJWT
from src.core.security import JWTBearer


def role_required(
    admin: bool = False,
    superuser: bool = False,
):
    def checker(user: UserJWT = Depends(JWTBearer())):
        if admin and user.is_admin:
            return user
        if superuser and user.is_superuser:
            return user
        if admin and superuser and (user.is_admin or user.is_superuser):
            return user
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав"
        )
    return checker