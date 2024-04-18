"""
Модуль CRUD операций модели 'CharityProject'.
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):
    """Класс CRUD операций модели 'CharityProject'."""

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ):
        """Получение объекта CharityProject по имени."""
        charity_project = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        charity_project = charity_project.scalars().first()

        return charity_project


charity_project_crud = CRUDCharityProject(CharityProject)
