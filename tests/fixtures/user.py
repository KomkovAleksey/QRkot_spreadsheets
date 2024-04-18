import pytest
from conftest import (
    app, current_superuser, current_user, get_async_session, override_db
)
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.models.user import User

superuser = User(
    id=1,
    is_active=True,
    is_verified=True,
    is_superuser=True,
)

user = User(
    id=2,
    is_active=True,
    is_verified=True,
    is_superuser=False,
)

not_auth_user = User(
    id=3,
    is_active=False,
    is_verified=False,
    is_superuser=False,
)


@pytest.fixture
def user_client():
    def raise_forbidden():
        raise HTTPException(status_code=403, detail='Forbidden')

    app.dependency_overrides = {}
    app.dependency_overrides[get_async_session] = override_db
    app.dependency_overrides[current_user] = lambda: user
    app.dependency_overrides[current_superuser] = (
        lambda: raise_forbidden()
    )
    with TestClient(app) as client:
        yield client


@pytest.fixture
def test_client():
    app.dependency_overrides = {}
    app.dependency_overrides[get_async_session] = override_db
    app.dependency_overrides[current_user] = lambda: not_auth_user
    with TestClient(app) as client:
        yield client


@pytest.fixture
def superuser_client():
    app.dependency_overrides = {}
    app.dependency_overrides[get_async_session] = override_db
    app.dependency_overrides[current_superuser] = lambda: superuser
    with TestClient(app) as client:
        yield client
