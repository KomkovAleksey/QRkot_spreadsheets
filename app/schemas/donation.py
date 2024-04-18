"""
Модуль схем 'Donation'.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class DonationCreate(BaseModel):
    """Схема создания 'Donation'."""

    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid
        orm_mode = True


class DonationDBShort(DonationCreate):
    """
    Короткая схема ответа из базы данных.
    Для зарегистрированного пользователя.
    """

    id: int
    create_date: datetime


class DonationDBFull(DonationDBShort):
    """Схема ответа из базы данных для суперпользователя."""

    id: int
    user_id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]
