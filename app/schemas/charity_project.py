from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator

NAME_IS_NONE = "Название не может быть пустым!"
DESCRIPTION_IS_NONE = "Описание не может быть пустым!"
AMOUNT_IS_NONE = "Необходимая сумма не может быть пустой!"


class CharityProjectBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: str
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid
        min_anystr_length = 1


class CharityProjectCreate(CharityProjectBase):
    invested_amount: int = 0


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt]

    @validator("name")
    def validate_name(cls, value):
        if value is None:
            raise ValueError(NAME_IS_NONE)
        return value

    @validator("description")
    def validate_description(cls, value):
        if value is None:
            raise ValueError(DESCRIPTION_IS_NONE)
        return value

    @validator("full_amount")
    def validate_full_amount(cls, value):
        if value is None:
            raise ValueError(AMOUNT_IS_NONE)
        return value


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int = 0
    fully_invested: bool = False
    create_date: datetime
    close_date: datetime = None

    class Config:
        orm_mode = True
