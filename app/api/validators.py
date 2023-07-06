from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate

PROJECT_EXISTS = "Проект с таким именем уже существует!"
PROJECT_NOT_EXISTS = "Проект с таким именем не найден!"
PROJECT_CLOSED = "Закрытый проект нельзя редактировать!"
AMOUNT_TOO_SMALL = "Нельзя установить сумму, ниже уже вложенной!"
DELETE_PERMISSION = "В проект были внесены средства, не подлежит удалению!"


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    """Проверяет уникальность названия проекта."""
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name,
        session
    )
    if project_id is not None:
        raise HTTPException(status_code=400, detail=PROJECT_EXISTS,)


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """Проверяет существует ли проект"""
    charity_project = await charity_project_crud.get(
        charity_project_id,
        session
    )
    if charity_project is None:
        raise HTTPException(status_code=404, detail=PROJECT_NOT_EXISTS)
    return charity_project


def check_charity_project_close(
    project: CharityProject,
) -> None:
    """Проверяет, закрыт ли проект."""
    if project.fully_invested:
        raise HTTPException(status_code=400, detail=PROJECT_CLOSED)


def check_invested_before_edit(
    project: CharityProject,
    project_request: CharityProjectUpdate,
) -> None:
    """Проверяет сумму, инвестированную в проект при обновлении проекта."""
    if (
        project_request.full_amount is not None and
        project.invested_amount > project_request.full_amount
    ):
        raise HTTPException(status_code=400, detail=AMOUNT_TOO_SMALL)


def check_invested_before_delete(
    project: CharityProject,
) -> None:
    """Проверяет сумму, инвестированную в проект при удалении проекта."""
    if project.invested_amount > 0:
        raise HTTPException(status_code=400, detail=DELETE_PERMISSION)
