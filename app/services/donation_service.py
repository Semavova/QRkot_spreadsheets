from datetime import datetime
from typing import List

from app.models.base import Fund


def investment(
    target: Fund,
    sources: List[Fund],
) -> List[Fund]:
    """
    Перебирает открытые проекты/донаты, вычисляет сумму перевода.
    Переводит средства из донатов в проекты.
    Закрывает исчерпанные донаты и заполненные проекты.
    """
    modified = []
    for source in sources:
        fund = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount
        )
        if not fund:
            break
        for investment in [target, source]:
            investment.invested_amount += fund
            if investment.invested_amount == investment.full_amount:
                investment.fully_invested = True
                investment.close_date = datetime.now()
        modified.append(source)
    return modified
