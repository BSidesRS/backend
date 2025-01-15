import ormar.exceptions
from fastapi import Depends, Header, HTTPException
from freenit.api.router import route
from freenit.models.user import User
from freenit.permissions import user_perms
from freenit.models.pagination import Page, paginate

from ..models.presentation import Presentation, PresentationOptional

tags = ["presentation"]


@route("/{conference}/presentations", tags=tags)
class PresentationListAPI:
    @staticmethod
    async def get(
        page: int = Header(default=1),
        perpage: int = Header(default=10),
    ) -> Page[Presentation]:
        return await paginate(Presentation.objects, page, perpage)

    @staticmethod
    async def post(
        presentation: Presentation,
        user: User = Depends(user_perms),
    ) -> Presentation:
        presentation.user = user
        await presentation.save()
        return presentation


@route("/presentations/{id}", tags=tags)
class PresentationDetailAPI:
    @staticmethod
    async def get(id: int) -> Presentation:
        try:
            presentation = await Presentation.objects.get(pk=id)
        except ormar.exceptions.NoMatch:
            raise HTTPException(status_code=404, detail="No such presentation")
        return presentation

    @staticmethod
    async def patch(
        id: int,
        presentation_data: PresentationOptional,
        user: User = Depends(user_perms),
    ) -> Presentation:
        try:
            presentation = await Presentation.objects.get(pk=id)
            if not user.admin and presentation.user.id != user.id:
                raise HTTPException(
                    status_code=403, detail="Presentation blongs to somebody else?"
                )
            await presentation.patch(presentation_data)
        except ormar.exceptions.NoMatch:
            raise HTTPException(status_code=404, detail="No such presentation")
        return presentation

    @staticmethod
    async def delete(
        id: int,
        user: User = Depends(user_perms),
    ) -> Presentation:
        try:
            presentation = await Presentation.objects.get(pk=id)
            if not user.admin and presentation.user.id != user.id:
                raise HTTPException(
                    status_code=403, detail="Presentation blongs to somebody else?"
                )
        except ormar.exceptions.NoMatch:
            raise HTTPException(status_code=404, detail="No such presentation")
        await presentation.delete()
        return presentation
