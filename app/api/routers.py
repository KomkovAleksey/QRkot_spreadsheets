"""
Модуль роутеров.
"""
from fastapi import APIRouter

from app.api.endpoints import (
    charity_project_router,
    donation_router,
    user_router,
)

main_router = APIRouter()
main_router.include_router(
    charity_project_router, prefix='/charity_project', tags=['Charity Project']
)
main_router.include_router(
    donation_router, prefix='/donation', tags=['Donation']
)
main_router.include_router(user_router)
