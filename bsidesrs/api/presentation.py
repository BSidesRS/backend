import ormar.exceptions
from fastapi import Depends, Header, HTTPException
from freenit.api.router import route
from freenit.models.user import User
from freenit.permissions import user_perms
from freenit.models.pagination import Page, paginate

from ..models.conference import Conference
from ..models.presentation import Presentation, PresentationOptional, PresentationSafe

tags = ["presentation"]


@route("/{conference}/presentations", tags=tags)
class PresentationListAPI:
    @staticmethod
    async def get(
        conference: str,
        page: int = Header(default=1),
        perpage: int = Header(default=10),
    ) -> Page[PresentationSafe]:
        try:
            conf = await Conference.objects.select_related("rooms").get(name=conference)
        except ormar.exceptions.NoMatch:
            raise HTTPException(status_code=404, detail="No such conference")
        query = Presentation.objects.select_related(["day", "room", "user"]).filter(
            room__in=[r.pk for r in conf.rooms]
        )
        return await paginate(query, page, perpage)

    @staticmethod
    async def post(
        conference: str,
        presentation: Presentation,
        user: User = Depends(user_perms),
    ) -> PresentationSafe:
        try:
            conf = await Conference.objects.select_related("rooms").get(name=conference)
        except ormar.exceptions.NoMatch:
            raise HTTPException(status_code=404, detail="No such conference")
        if len(conf.rooms) == 0:
            raise HTTPException(status_code=409, detail="Conference has no rooms")
        presentation.user = user
        presentation.room = conf.rooms[0]
        await presentation.save()
        return presentation


@route("/presentations/{id}", tags=tags)
class PresentationDetailAPI:
    @staticmethod
    async def get(id: int) -> PresentationSafe:
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
    ) -> PresentationSafe:
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
    ) -> PresentationSafe:
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
