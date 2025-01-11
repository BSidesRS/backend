from typing import List

import ormar
import ormar.exceptions
from fastapi import Depends, HTTPException
from freenit.api.router import route
from freenit.models.user import User
from freenit.permissions import user_perms

from ..models.conference import Conference
from ..models.day import Day, DayOptional

tags = ["day"]


@route("/{conference}/days", tags=tags)
class DayListAPI:
    @staticmethod
    async def get(conference: str) -> List[Day]:
        try:
            conf = await Conference.objects.get(name=conference)
        except ormar.exceptions.NoMatch:
            raise HTTPException(status_code=404, detail="No such conference")
        return conf.days

    @staticmethod
    async def post(
        conference: str,
        day: Day,
        user: User = Depends(user_perms),
    ) -> Day:
        if not user.admin:
            raise HTTPException(status_code=403, detail="Only admins can create days")
        try:
            day.conference = await Conference.objects.get(name=conference)
        except ormar.exceptions.NoMatch:
            raise HTTPException(status_code=404, detail="No such conference")
        await day.save()
        return day


@route("/days/{id}", tags=tags)
class DayDetailAPI:
    @staticmethod
    async def get(id: int) -> Day:
        try:
            day = await Day.objects.get(pk=id)
        except ormar.exceptions.NoMatch:
            raise HTTPException(status_code=404, detail="No such day")
        return day

    @staticmethod
    async def patch(
        id: int,
        day_data: DayOptional,
        user: User = Depends(user_perms),
    ) -> Day:
        if not user.admin:
            raise HTTPException(status_code=403, detail="Only admins can edit days")
        try:
            day = await Day.objects.get(pk=id)
            await day.patch(day_data)
        except ormar.exceptions.NoMatch:
            raise HTTPException(status_code=404, detail="No such day")
        return day

    @staticmethod
    async def delete(id: int, user: User = Depends(user_perms)) -> Day:
        if not user.admin:
            raise HTTPException(status_code=403, detail="Only admins can delete days")
        try:
            day = await Day.objects.get(pk=id)
        except ormar.exceptions.NoMatch:
            raise HTTPException(status_code=404, detail="No such day")
        await day.delete()
        return day
