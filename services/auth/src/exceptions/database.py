class DatabaseException(Exception):
    """
    Базовое исключение для всех ошибок базы данных
    """

    def __init__(self, message: str, *args: object) -> None:
        self.message = message
        super().__init__(message, *args)


class RecordNotFoundError(DatabaseException):
    """
    Ошибка, возникающая, если запись не найдена
    """
    pass


class IntegrityError(DatabaseException):
    """
    Ошибка целостности данных
    """
    pass