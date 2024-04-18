from pathlib import Path

import pytest
import pytest_asyncio
from mixer.backend.sqlalchemy import Mixer as _mixer
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

try:
    from app.main import app  # noqa
except (NameError, ImportError) as error:
    raise AssertionError(
        'При импорте объекта приложения `app` из модуля `app.main` '
        f'возникло исключение:\n{type(error).__name__}: {error}.'
    )

try:
    from app.core.db import Base, get_async_session  # noqa
except (NameError, ImportError) as error:
    raise AssertionError(
        'При импорте объектов `Base, get_async_session` '
        'из модуля `app.core.db` возникло исключение:\n'
        f'{type(error).__name__}: {error}.'
    )

try:
    from app.core.user import current_superuser, current_user  # noqa
except (NameError, ImportError) as error:
    raise AssertionError(
        'При импорте объектов `current_superuser, current_user` '
        'из модуля `app.core.user` возникло исключение:\n'
        f'{type(error).__name__}: {error}.'
    )

try:
    from app.schemas.user import UserCreate  # noqa
except (NameError, ImportError) as error:
    raise AssertionError(
        'При импорте схемы `UserCreate` из модуля `app.schemas.user` '
        'возникло исключение:\n'
        f'{type(error).__name__}: {error}.'
    )


BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

pytest_plugins = [
    'fixtures.user',
    'fixtures.data',
]

TEST_DB = BASE_DIR / 'test.db'
SQLALCHEMY_DATABASE_URL = f'sqlite+aiosqlite:///{str(TEST_DB)}'
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False},
)
TestingSessionLocal = sessionmaker(
    class_=AsyncSession, autocommit=False, autoflush=False, bind=engine,
)


async def override_db():
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture(autouse=True)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def mixer():
    mixer_engine = create_engine(f'sqlite:///{str(TEST_DB)}')
    session = sessionmaker(bind=mixer_engine)
    return _mixer(session=session(), commit=True)
