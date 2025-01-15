import ormar.exceptions
from fastapi import Depends, Header, HTTPException
from freenit.api.router import route
from freenit.models.user import User
from freenit.permissions import user_perms
from freenit.models.pagination import Page, paginate

from ..models.conference import Conference, ConferenceOptional
from ..models.day import Day
from ..models.room import Room

tags = ["conference"]


@route("/conferences", tags=tags)
class ConferenceListAPI:
    @staticmethod
    async def get(
        page: int = Header(default=1),
        perpage: int = Header(default=10),
    ) -> Page[Conference]:
        return await paginate(Conference.objects, page, perpage)

    @staticmethod
    async def post(
        conference: Conference,
        user: User = Depends(user_perms),
    ) -> Conference:
        if not user.admin:
            raise HTTPException(
                status_code=403, detail="Only admins can create conferences"
            )
        await conference.save()
        day = Day(conference=conference)
        await day.save()
        room = Room(name="room1", conference=conference)
        await room.save()
        await conference.load_all()
        return conference


@route("/conferences/{id}", tags=tags)
class ConferenceDetailAPI:
    @staticmethod
    async def get(id: int) -> Conference:
        try:
            conference = await Conference.objects.get(pk=id)
        except ormar.exceptions.NoMatch:
            raise HTTPException(status_code=404, detail="No such conference")
        return conference

    @staticmethod
    async def patch(
        id: int,
        conference_data: ConferenceOptional,
        user: User = Depends(user_perms),
    ) -> Conference:
        if not user.admin:
            raise HTTPException(
                status_code=403, detail="Only admins can edit conferences"
            )
        try:
            conference = await Conference.objects.get(pk=id)
            await conference.patch(conference_data)
        except ormar.exceptions.NoMatch:
            raise HTTPException(status_code=404, detail="No such conference")
        return conference

    @staticmethod
    async def delete(
        id: int,
        user: User = Depends(user_perms),
    ) -> Conference:
        if not user.admin:
            raise HTTPException(
                status_code=403, detail="Only admins can delete conferences"
            )
        try:
            conference = await Conference.objects.get(pk=id)
        except ormar.exceptions.NoMatch:
            raise HTTPException(status_code=404, detail="No such conference")
        await conference.delete()
        return conference
