from typing import List

from pydantic import BaseModel

from app.library.doorplates import Doorplate


class DoorplateRequest(BaseModel):
    roomnumber: str
    description: str
    personname: str
    template: str


class DoorplateResponse(BaseModel):
    id: str
    roomnumber: str
    description: str
    personname: str
    template: str


class DoorplatesResponse(BaseModel):
    id: str
    doorplates: List[DoorplateResponse]


async def to_doorplate(doorplate_request: DoorplateRequest) -> Doorplate:
    return Doorplate(
        id=None,
        roomnumber=doorplate_request.roomnumber,
        description=doorplate_request.description,
        personname=doorplate_request.personname,
        template=doorplate_request.template,
    )


async def to_doorplate_response(doorplate: Doorplate) -> DoorplateResponse:
    return DoorplateResponse(
        id=doorplate.id,
        roomnumber=doorplate.roomnumber,
        description=doorplate.description,
        personname=doorplate.personname,
        template=doorplate.template,
    )
