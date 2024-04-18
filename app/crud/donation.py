"""
Модуль CRUD операций модели 'Donation'.
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):
    """Класс CRUD операций модели 'Donation'."""

    async def get_by_user(
        self,
        user: User,
        session: AsyncSession,
    ):
        """
        Получение списка объектов Donation,
        сделанных пользователем.
        """
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )

        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
