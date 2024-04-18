from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import ErrorText
from app.crud import charity_project_crud


async def get_object_from_db(
    obj_id: int,
    session: AsyncSession,
):
    """
    Достает обьект из бд.
    Если его нет вызывает исключение.
    """
    charity_project = await charity_project_crud.get(
        obj_id,
        session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=ErrorText.PROJECT_NOT_FOUND
        )

    return charity_project
