class BaseException(Exception):
    """
    Базовое исключение приложения
    """
    def __init__(self, message: str, *args: object) -> None:
        super().__init__(message, *args)


class NotFoundException(BaseException):
    """
    Объект не найден
    """
    def __init__(self, message: str, *args: object) -> None:
        super().__init__(message, *args)