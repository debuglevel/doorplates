from pydantic import BaseModel

# TODO should also have internal representation


class DoorplateIn(BaseModel):
    roomnumber: str
    description: str
    personname: str
    template: str


class DoorplateOut(BaseModel):
    id: str
