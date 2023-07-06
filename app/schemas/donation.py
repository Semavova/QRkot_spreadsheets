from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class DonationBase(BaseModel):
    comment: Optional[str]
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    invested_amount: int = 0


class DonationDB(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationAdminDB(DonationDB):
    user_id: int
    invested_amount: int = 0
    fully_invested: bool = False
    close_date: datetime = None
