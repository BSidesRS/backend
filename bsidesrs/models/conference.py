import ormar
from freenit.models.sql.base import OrmarBaseModel, make_optional, ormar_config


class Conference(OrmarBaseModel):
    ormar_config = ormar_config.copy()

    id = ormar.Integer(primary_key=True)
    name = ormar.Text(index=True, unique=True)


class ConferenceOptional(Conference):
    pass


make_optional(ConferenceOptional)
