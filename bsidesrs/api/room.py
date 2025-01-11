from typing import List

import ormar
import ormar.exceptions
from fastapi import Depends, HTTPException
from freenit.api.router import route
from freenit.models.user import User
from freenit.permissions import user_perms

from ..models.conference import Conference
from ..models.room import Room, RoomOptional

tags = ["room"]


@route("/{conference}/rooms", tags=tags)
class RoomListAPI:
    @staticmethod
    async def get(conference: str) -> List[Room]:
        try:
            conf = await Conference.objects.get(name=conference)
        except ormar.exceptions.NoMatch:
            raise HTTPException(status_code=404, detail="No such conference")
        return conf.rooms

    @staticmethod
    async def post(
        conference: str,
        room: Room,
        user: User = Depends(user_perms),
    ) -> Room:
        if not user.admin:
            raise HTTPException(status_code=403, detail="Only admins can create rooms")
        try:
            room.conference = await Conference.objects.get(name=conference)
        except ormar.exceptions.NoMatch:
            raise HTTPException(status_code=404, detail="No such conference")
        await room.save()
        return room


@route("/rooms/{id}", tags=tags)
class RoomDetailAPI:
    @staticmethod
    async def get(id: int) -> Room:
        try:
            room = await Room.objects.get(pk=id)
        except ormar.exceptions.NoMatch:
            raise HTTPException(status_code=404, detail="No such room")
        return room

    @staticmethod
    async def patch(
        id: int,
        room_data: RoomOptional,
        user: User = Depends(user_perms),
    ) -> Room:
        if not user.admin:
            raise HTTPException(status_code=403, detail="Only admins can edit rooms")
        try:
            room = await Room.objects.get(pk=id)
            await room.patch(room_data)
        except ormar.exceptions.NoMatch:
            raise HTTPException(status_code=404, detail="No such room")
        return room

    @staticmethod
    async def delete(id: int, user: User = Depends(user_perms)) -> Room:
        if not user.admin:
            raise HTTPException(status_code=403, detail="Only admins can delete rooms")
        try:
            room = await Room.objects.get(pk=id)
        except ormar.exceptions.NoMatch:
            raise HTTPException(status_code=404, detail="No such room")
        await room.delete()
        return room
