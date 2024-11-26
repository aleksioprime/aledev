from pydantic import BaseModel


class RegisterSchema(BaseModel):
    """
    Схема для регистрации пользователя. Определяет поля, необходимые для создания нового пользователя
    """
    login: str
    password: str
    first_name: str
    last_name: str

    class Config:
        from_attributes = True


class AuthSchema(BaseModel):
    """
    Схема для аутентификации пользователя. Определяет поля, необходимые для входа в систему
    """
    login: str
    password: str