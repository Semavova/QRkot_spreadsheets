from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import charity_project_crud, donation_crud
from app.models import User
from app.schemas.donation import DonationAdminDB, DonationCreate, DonationDB
from app.services import investment

GET_DONATIONS = "Получить список всех пожертвований."
CREATE_DONATION = "Сделать пожертвование."
GET_MY_DONATIONS = "Получить список моих пожертвований."

router = APIRouter()


@router.get(
    "/",
    response_model=List[DonationAdminDB],
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
    summary=GET_DONATIONS,
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
) -> DonationAdminDB:
    """
    Только для суперюзеров.\n
    Получает список всех пожертвований.
    """
    all_donations = await donation_crud.get_all(session)
    return all_donations


@router.post(
    "/",
    response_model=DonationDB,
    response_model_exclude_none=True,
    summary=CREATE_DONATION,
)
async def create_donation(
    donation: DonationCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
) -> DonationDB:
    """Создает пожертвование."""
    new_donation = await donation_crud.create(
        donation,
        session,
        user,
        commit=False
    )
    session.add_all(
        investment(
            new_donation, await charity_project_crud.get_opened(session)
        )
    )
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get(
    "/my",
    response_model=List[DonationDB],
    response_model_exclude_none=True,
    summary=GET_MY_DONATIONS,
)
async def get_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
) -> DonationDB:
    """Возвращает список пожертвований текущего пользователя."""
    donations = await donation_crud.get_by_user(user, session)
    return donations
