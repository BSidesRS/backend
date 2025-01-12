import ormar
from freenit.models.sql.base import OrmarBaseModel, make_optional, ormar_config
from .conference import Conference


class Room(OrmarBaseModel):
    ormar_config = ormar_config.copy()

    id = ormar.Integer(primary_key=True)
    name = ormar.Text(index=True)
    conference = ormar.ForeignKey(Conference)


class RoomOptional(Room):
    pass


make_optional(RoomOptional)
