from typing import List

import ormar
import ormar.exceptions
from fastapi import HTTPException
from freenit.api.router import route

from ..models.presentation import Presentation, PresentationOptional

tags=['presentation']


@route('/presentations', tags=tags)
class PresentationListAPI():
    @staticmethod
    async def get() -> List[Presentation]:
        return await Presentation.objects.all()

    @staticmethod
    async def post(presentation: Presentation) -> Presentation:
        await presentation.save()
        return presentation


@route('/presentations/{id}', tags=tags)
class PresentationDetailAPI():
    @staticmethod
    async def get(id: int) -> Presentation:
        try:
            presentation = await Presentation.objects.get(pk=id)
        except ormar.exceptions.NoMatch:
            raise HTTPException(status_code=404, detail="No such presentation")
        return presentation

    @staticmethod
    async def patch(id: int, presentation_data: PresentationOptional) -> Presentation:
        try:
            presentation = await Presentation.objects.get(pk=id)
            await presentation.patch(presentation_data)
        except ormar.exceptions.NoMatch:
            raise HTTPException(status_code=404, detail="No such presentation")
        return presentation

    @staticmethod
    async def delete(id: int) -> Presentation:
        try:
            presentation = await Presentation.objects.get(pk=id)
        except ormar.exceptions.NoMatch:
            raise HTTPException(status_code=404, detail="No such presentation")
        await presentation.delete()
        return presentation
