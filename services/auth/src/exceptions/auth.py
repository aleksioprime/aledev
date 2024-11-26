class AuthException(Exception):
    """
    Базовое исключение для всех ошибок аутентификации
    """

    def __init__(self, message: str, *args: object) -> None:
        self.message = message
        super().__init__(message, *args)


class RegisterError(AuthException):
    """
    Ошибка регистрации
    """
    pass


class LoginError(AuthException):
    """
    Ошибка аутентификации
    """
    pass


class TokenValidationError(AuthException):
    """
    Ошибка проверки токена
    """
    pass
