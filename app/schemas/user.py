"""
Модуль схем 'User'.
"""
from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Схема чтения 'User'."""
    pass


class UserCreate(schemas.BaseUserCreate):
    """Схема создания 'User'."""
    pass


class UserUpdate(schemas.BaseUserUpdate):
    """Схема обновления 'User'."""
    pass
