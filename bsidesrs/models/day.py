import ormar
from freenit.models.sql.base import OrmarBaseModel, make_optional, ormar_config
from .conference import Conference


class Day(OrmarBaseModel):
    ormar_config = ormar_config.copy()

    id = ormar.Integer(primary_key=True)
    date = ormar.Date()
    conference = ormar.ForeignKey(Conference, related_name="days")


class DayOptional(Day):
    pass


make_optional(DayOptional)
