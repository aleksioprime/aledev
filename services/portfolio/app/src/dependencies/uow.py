from src.repositories.uow import UnitOfWork


async def get_unit_of_work():
    """
    Возвращает новый Unit of Work
    """
    return UnitOfWork()