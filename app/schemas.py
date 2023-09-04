from pydantic import BaseModel


class UserData(BaseModel):
    id: int


class EventMessage(BaseModel):
    message: str
