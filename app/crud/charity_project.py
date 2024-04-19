"""
Модуль CRUD операций модели 'CharityProject'.
"""
from sqlalchemy import select, extract
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):
    """Класс CRUD операций модели 'CharityProject'."""

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> CharityProject:
        """Получение объекта CharityProject по имени."""
        charity_project = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        charity_project = charity_project.scalars().first()

        return charity_project

    async def get_projects_by_completion_rate(
        session: AsyncSession
    ) -> list[CharityProject]:
        """
        Возвращает список проектов отсортированный
        по времени понадобившимся для сбора средств.
        """
        completion_rate = extract(
            'epoch', CharityProject.close_date
        ) - extract('epoch', CharityProject.create_date)
        projects = await session.execute(
            select(CharityProject).where(CharityProject.fully_invested)
        ).order_by(completion_rate)
    
        return projects.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)
