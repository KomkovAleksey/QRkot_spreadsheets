"""
Модуль настроек проекта 'QRKot'.
"""
from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    """Класс настроек проекта 'QRKot'."""

    app_title: str = 'QRKot'
    app_description: str = 'Приложение сбора пожертвований для котиков'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
