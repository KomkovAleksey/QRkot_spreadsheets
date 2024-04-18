"""
Модуль эндпоинтов модели 'CharityProject' приложения 'QRKot'.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.utils import get_object_or_404
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectDB,
    CharityProjectCreate,
    CharityProjectUpdate,
)
from app.services import investmentService

router = APIRouter()


@router.post(
    "/",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    obj_in: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    POST-запрос на создание благотворительного проекта.
    Только для суперюзеров.
    """
    return await investmentService(
        session
    ).create_charity_project(obj_in)


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_project(
    session: AsyncSession = Depends(get_async_session),
):
    """GET-запрос на получение списка всех благотворительных проектов."""
    return await charity_project_crud.get_multi(session)


@router.delete(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    DELETE-запрос на удаление благотворительного проекта.
    Только для суперюзеров.
    """
    charity_project = await get_object_or_404(project_id, session)
    return await investmentService(
        session
    ).remove_charity_project(charity_project)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    PATCH-запрос на редактирование благотворительного проекта.
    Только для суперюзеров.
    """
    charity_project = await get_object_or_404(project_id, session)
    return await investmentService(
        session
    ).update_charity_project(project_id, obj_in, charity_project)
