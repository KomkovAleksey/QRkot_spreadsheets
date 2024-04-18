"""
Модуль эндпоинтов для взаимодействия с `Google API`
"""
from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.schemas.charity_project import CharityProjectDB
from app.crud.charity_project import charity_project_crud
from app.services.google_service import (
    set_user_permissions,
    spreadsheets_create,
    spreadsheets_update_value,
)

router = APIRouter()


@router.post(
    '/',
    response_model=list[CharityProjectDB],
    dependencies=[Depends(current_superuser)],
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)

):
    """
    Создание отчёта в Google таблицу
    с закрытыми проектами отсортированными
    по времени затраченному на сбор средств.
    Только для суперюзеров.
    """
    project = await charity_project_crud.get_projects_by_completion_rate(
        session
    )
    spreadsheetid = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheetid, wrapper_services)
    await spreadsheets_update_value(
        spreadsheetid,
        project,
        wrapper_services,
    )

    return project
