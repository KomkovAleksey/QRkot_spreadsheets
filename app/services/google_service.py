"""
Сервис взаимодействия приложения 'QRKot' с Google API.
"""
from datetime import datetime

from typing import List
from aiogoogle import Aiogoogle

from app.models import CharityProject
from app.core.config import settings
from app.core.constants import FORMAT, COLUMNS, ROWS, RANGE


async def spreadsheets_create(wrapper_services: Aiogoogle):
    """Функция создания таблицы."""
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {'title': f'Отчёт от {now_date_time}',
                       'locale': 'ru_RU'},
        'sheets': [{'properties': {
            'sheetType': 'GRID',
            'sheetId': 0,
            'title': 'Лист1',
            'gridProperties': {'rowCount': ROWS, 'columnCount': COLUMNS}
        }}]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
):
    """
    Функция для предоставления прав доступа
    вашему личному аккаунту к созданному документу.
    """
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        projects: List[CharityProject],
        wrapper_services: Aiogoogle
):
    """
    Записывает полученную из базы данных информацию в документ с таблицами.
    """
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчёт от', now_date_time],
        ['Топ проектов по скорости закрытия.'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    for project in projects:
        new_row = [
            str(project.name),
            str(project.close_date - project.create_date),
            str(project.description),
        ]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=RANGE,
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
