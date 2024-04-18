"""
Модуль для создания пользователей.
"""
import contextlib

from fastapi_users.exceptions import UserAlreadyExists
from pydantic import EmailStr

from app.core.config import settings
from app.core.db import get_async_session
from app.core.user import get_user_db, get_user_manager
from app.schemas.user import UserCreate

get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(
        email: EmailStr,
        password: str,
        is_superuser: bool = False
):
    """
    Корутина, создающая юзера с переданным email и паролем.
    В случае, если такой пользователь уже есть, ничего не предпринимать.
    """
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    await user_manager.create(
                        UserCreate(
                            email=email,
                            password=password,
                            is_superuser=is_superuser
                        )
                    )
    except UserAlreadyExists:
        pass


async def create_first_superuser():
    """
    Корутина, проверяющая, указаны ли в настройках данные для суперюзера.
    Если да, то вызывается корутина create_user для создания суперпользователя.
    """
    if (
        settings.first_superuser_email is not None and
        settings.first_superuser_password is not None
    ):
        await create_user(
            email=settings.first_superuser_email,
            password=settings.first_superuser_password,
            is_superuser=True,
        )
