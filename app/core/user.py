"""
Модуль настройки аунтификации.
"""
from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
    IntegerIDMixin,
    InvalidPasswordException,
)
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.constants import (
    TOKEN_VALIdITY_PERIOD,
    MIN_LEN_PASSWORD,
    ErrorText,
)


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """
    Асинхронный генератор.
    Обеспечивает доступ к БД через SQLAlchemy.
    """
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    """Определяет стратегию: хранение токена в виде JWT."""
    return JWTStrategy(
        secret=settings.secret,
        lifetime_seconds=TOKEN_VALIdITY_PERIOD
    )


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        """Валидация пароля."""
        if len(password) < MIN_LEN_PASSWORD:
            raise InvalidPasswordException(
                reason=ErrorText.PASSWORD_TOO_SHORT
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason=ErrorText.EMAIL_IN_PASSWORD
            )

    async def on_after_register(
            self, user: User, request: Optional[Request] = None
    ):
        """Метод для действий после успешной регистрации пользователя."""
        print(f'Пользователь {user.email} зарегистрирован.')


async def get_user_manager(user_db=Depends(get_user_db)):
    """Корутина, возвращающая объект класса UserManager."""
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
