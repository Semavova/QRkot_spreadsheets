from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.db import Base

DESCRIPTION = (
    "Необходимая сумма: {full_amount}, "
    "Уже собрано: {invested_amount}, "
    "Использовано: {fully_invested}, "
    "Дата создания: {create_date}, "
    "Дата закрытия: {close_date}."
)


class Fund(Base):
    __abstract__ = True
    __table_args__ = (
        CheckConstraint('full_amount > 0', 'full_amount >= invested_amount'),
    )

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    close_date = Column(DateTime)

    def __repr__(self):
        return DESCRIPTION.format(
            full_amount=self.full_amount,
            invested_amount=self.invested_amount,
            fully_invested=self.fully_invested,
            create_date=self.create_date,
            close_date=self.close_date
        )
