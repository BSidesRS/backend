import ormar
from freenit.models.sql.base import OrmarBaseModel, make_optional, ormar_config
from freenit.models.user import User
from .day import Day
from .room import Room


class Presentation(OrmarBaseModel):
    ormar_config = ormar_config.copy()

    id = ormar.Integer(primary_key=True)
    title = ormar.Text()
    description = ormar.Text()
    user = ormar.ForeignKey(User)
    start = ormar.DateTime()
    duration = ormar.Integer()
    day = ormar.ForeignKey(Day)
    room = ormar.ForeignKey(Room)


class PresentationOptional(Presentation):
    pass


make_optional(PresentationOptional)
