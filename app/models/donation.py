"""
Модуль модели 'Donation'.
"""
from sqlalchemy import Column, Integer, Text, ForeignKey

from .abstract_model import AbstractProjectDonation


class Donation(AbstractProjectDonation):
    """Модель 'Donation'."""

    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
