from sqlalchemy import Column, String, Text

from app.models.base import Fund

DESCRIPTION = (
    "Название: {name}, "
    "Описание: {description}, "
    "{invested}"
)


class CharityProject(Fund):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return DESCRIPTION.format(
            name=self.name,
            description=self.description,
            invested=super().__repr__()
        )
