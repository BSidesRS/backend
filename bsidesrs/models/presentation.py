import ormar
from freenit.models.sql.base import (
    OrmarBaseModel,
    generate_optional,
    ormar_config,
)
from freenit.models.user import User


class Presentation(OrmarBaseModel):
    ormar_config = ormar_config.copy()

    id = ormar.Integer(primary_key=True)
    title = ormar.Text()
    description = ormar.Text()
    user = ormar.ForeignKey(User)
    start = ormar.DateTime()
    duration = ormar.Integer()
    

PresentationOptional = generate_optional(Presentation)
