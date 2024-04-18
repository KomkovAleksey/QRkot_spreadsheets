"""
Модуль CharityProjectService проекта 'QRKot'.
"""
from http import HTTPStatus
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.models import User
from app.models.abstract_model import AbstractProjectDonation
from app.core.constants import ErrorText, DEFAULT_INVESTED_AMOUNT
from app.core.user import current_user
from app.crud import charity_project_crud, donation_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpdate,
)
from app.schemas.donation import DonationCreate


class investmentService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def check_name_duplicate(
            self,
            obj_name: str,
    ):
        """
        Проверяет имя объекта на уникальность.
        """
        obj_id = await charity_project_crud.get_project_id_by_name(
            obj_name,
            self.session
        )
        if obj_id is not None:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=ErrorText.NAME_DUPLICATE,
            )

    async def check_unclosed_donation(
            self,
            charity_project,
    ):
        """
        Ищет в бд открытые проекты.
        Запускает процесс инвестирования если находит.
        """
        unclosed_donation = await donation_crud.get_opened(self.session)
        if unclosed_donation:
            invested = self.investment(charity_project, unclosed_donation)
            self.session.add_all(invested)
        await self.session.commit()
        await self.session.refresh(charity_project)

    def investment(
        self,
        target: AbstractProjectDonation,
        sources: list[AbstractProjectDonation],
    ):
        """Инвестирование в незакрытые проекты."""
        changed = []
        for source in sources:
            for_invest = target.full_amount - target.invested_amount
            investitions = source.full_amount - source.invested_amount
            to_invest = min(for_invest, investitions)
            source.invested_amount += to_invest
            target.invested_amount += to_invest
            if source.full_amount == source.invested_amount:
                source.fully_invested = True
                source.close_date = datetime.now()
            if target.full_amount == target.invested_amount:
                target.fully_invested = True
                target.close_date = datetime.now()
                break
            changed.append(source)

        return changed

    async def check_charity_project_fully_invested(
        self,
        obj_id: int,
    ):
        """Проверка был ли проект полностью проинвестирован."""
        charity_project = await charity_project_crud.get(
            obj_id,
            self.session
        )
        if charity_project.fully_invested is True:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=ErrorText.PROJECT_CLOSED,
            )

    async def check_charity_project_was_invested(
        self,
        charity_project,
    ):
        """Проверка были ли вложены инвестиции в проект."""
        if charity_project.fully_invested or (
            charity_project.invested_amount
        ) > DEFAULT_INVESTED_AMOUNT:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=ErrorText.PROJECT_WITH_FUNDS,
            )

    async def check_new_full_amount(
        self,
        charity_project_id: int,
        data_in: CharityProjectUpdate,
    ):
        """
        Проверка чтобы новая полная сумма проекта не была ниже
        уже инвестированной в проект суммы пожертвований.
        """
        charity_project = await charity_project_crud.get(
            charity_project_id,
            self.session
        )
        if data_in.full_amount < charity_project.invested_amount:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=ErrorText.FULL_AMOUNT_ERROR,
            )

    async def remove_charity_project(
        self,
        charity_project,
    ):
        """Удаление благотворительного проекта из бд."""
        await self.check_charity_project_was_invested(charity_project)

        return await charity_project_crud.remove(charity_project, self.session)

    async def update_charity_project(
        self,
        project_id,
        obj_in: CharityProjectUpdate,
        charity_project,
    ):
        """Редактирование благотворительного проекта."""
        await self.check_charity_project_fully_invested(project_id)
        if obj_in.name:
            await self.check_name_duplicate(obj_in.name)
        if obj_in.full_amount:
            await self.check_new_full_amount(project_id, obj_in)

        charity_project = await charity_project_crud.update(
            charity_project,
            obj_in,
            self.session
        )
        await self.check_unclosed_donation(charity_project)

        return charity_project

    async def create_charity_project(
        self,
        charity_project: CharityProjectCreate,
    ):
        """Создание благотворительного проекта."""
        await self.check_name_duplicate(charity_project.name)
        charity_project = await charity_project_crud.create(
            charity_project,
            self.session
        )
        await self.check_unclosed_donation(charity_project)

        return charity_project

    async def create_donation(
        self,
        obj_in: DonationCreate,
        user: User = Depends(current_user)
    ):
        """Создание пожертвования."""
        donation = await donation_crud.create(obj_in, self.session, user)
        self.session.add_all(
            self.investment(
                donation,
                await charity_project_crud.get_opened(self.session)
            )
        )
        await self.session.commit()
        await self.session.refresh(donation)

        return donation
