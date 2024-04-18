"""
Модуль абстрактной моделей для приложения QRKot.
"""
from datetime import datetime

from sqlalchemy import Column, Integer, Boolean, DateTime

from app.core.db import Base
from app.core.constants import DEFAULT_INVESTED_AMOUNT, DEFAULT_FULLY_INVESTED


class AbstractProjectDonation(Base):
    """Абстрактнрый модель для моделей 'CharityProject' и 'Donation'."""

    __abstract__ = True
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=DEFAULT_INVESTED_AMOUNT)
    fully_invested = Column(Boolean, default=DEFAULT_FULLY_INVESTED)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)
