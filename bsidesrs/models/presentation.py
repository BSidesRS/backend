import datetime
import ormar
from freenit.models.sql.base import OrmarBaseModel, make_optional, ormar_config
from freenit.models.user import User

from .day import Day
from .room import Room


def now():
    n = datetime.datetime.now()
    t = datetime.time(n.hour, n.minute)
    return t


class Presentation(OrmarBaseModel):
    ormar_config = ormar_config.copy()

    id = ormar.Integer(primary_key=True)
    title = ormar.Text()
    description = ormar.Text()
    user = ormar.ForeignKey(User, ondelete="CASCADE")
    start = ormar.Time(default=now)
    duration = ormar.Integer()
    day = ormar.ForeignKey(Day, ondelete="CASCADE")
    room = ormar.ForeignKey(Room, ondelete="CASCADE")


class PresentationOptional(Presentation):
    pass


make_optional(PresentationOptional)
PresentationSafe = Presentation.get_pydantic(exclude={"user__password"})
