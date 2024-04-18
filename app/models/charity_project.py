"""
Модуль модели 'CharityProject'.
"""
from sqlalchemy import Column, String, Text

from .abstract_model import AbstractProjectDonation
from app.core.constants import MAX_PROJECT_NAME_LENGTH


class CharityProject(AbstractProjectDonation):
    """Модель 'CharityProject'."""

    name = Column(
        String(MAX_PROJECT_NAME_LENGTH),
        unique=True,
        nullable=False,
    )
    description = Column(Text, nullable=False)
