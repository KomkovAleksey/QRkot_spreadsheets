"""
Модуль эндпоинтов модели 'Donation' приложения 'QRKot'.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud import donation_crud
from app.models import User
from app.services import CharityProjectService
from app.schemas.donation import (
    DonationDBFull,
    DonationDBShort,
    DonationCreate,
)

router = APIRouter()


@router.get(
    "/",
    response_model=list[DonationDBFull],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """
    GET-запрос на получение списка всех пожертвований.
    Только для суперюзеров.
    """
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=list[DonationDBShort],
    response_model_exclude={'invested_amount'},
    response_model_exclude_none=True
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """GET-запрос на получение списка пожертвований пользователя."""
    return await donation_crud.get_by_user(user, session)


@router.post(
    '/',
    response_model=DonationDBShort,
    response_model_exclude_none=True
)
async def create_donation(
    obj_in: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """POST-запрос на создание пожертвования."""
    return await CharityProjectService(session).create_donation(obj_in, user)
