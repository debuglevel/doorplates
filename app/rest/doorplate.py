from pydantic import BaseModel

class DoorplateIn(BaseModel):
    roomnumber: str
    description: str
    personname: str
    template: str

class DoorplateOut(BaseModel):
    id: str