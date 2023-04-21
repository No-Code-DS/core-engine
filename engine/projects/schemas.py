import datetime
from pydantic import BaseModel, EmailStr, Field


class BaseProject(BaseModel):
    id: int
    project_name: str
    description: str
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class BaseUser(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class FullProject(BaseProject):
    users: list[BaseUser]
