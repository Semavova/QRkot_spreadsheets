from datetime import datetime
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import Boolean, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def get_all(
        self,
        session: AsyncSession,
    ):
        """Возвращает все объекты из БД текущей модели."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
        self,
        obj_in,
        session: AsyncSession,
        user: Optional[User] = None,
        commit: Optional[Boolean] = True,
    ):
        """Создает объект текущей модели."""
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        if commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ):
        """Возвращает объект из БД по id"""
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def get_opened(
            self,
            session: AsyncSession,
    ):
        """Возвращает незавершенные объекты из БД"""
        opened_objs = await session.execute(
            select(self.model).where(self.model.fully_invested is not True)
        )
        return opened_objs.scalars().all()

    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession,
    ):
        """Обновляет объект и возвращает обновленный объект."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict()
        for field in obj_data:
            if field in update_data and update_data[field] is not None:
                setattr(db_obj, field, update_data[field])
        if db_obj.full_amount == db_obj.invested_amount:
            db_obj.fully_invested = True
            db_obj.close_date = datetime.now()
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj,
        session: AsyncSession,
    ):
        """Удаляет объект по id."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj
