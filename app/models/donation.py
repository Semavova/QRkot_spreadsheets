from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import Fund

DESCRIPTION = (
    "Пользователь: {user_id}, "
    "Комментарий: {comment}, "
    "{invested}"
)


class Donation(Fund):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self):
        return DESCRIPTION.format(
            user_id=self.user_id,
            comment=self.comment,
            invested=super().__repr__()
        )
