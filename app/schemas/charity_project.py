"""
Модуль схем 'CharityProject'.
"""
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, PositiveInt, Extra

from app.core.constants import MAX_PROJECT_NAME_LENGTH, MIN_ANYSTR_LENGTH


class CharityProjectUpdate(BaseModel):
    """Схема обновления 'CharityProject'."""

    name: Optional[str] = Field(
        None,
        max_length=MAX_PROJECT_NAME_LENGTH,
    )
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid
        min_anystr_length = MIN_ANYSTR_LENGTH


class CharityProjectCreate(CharityProjectUpdate):
    """Схема создания 'CharityProject'."""

    name: str = Field(max_length=MAX_PROJECT_NAME_LENGTH)
    description: str
    full_amount: PositiveInt


class CharityProjectDB(CharityProjectUpdate):
    """Схема ответа из базы данных."""

    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
