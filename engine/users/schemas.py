from typing import Optional
from fastapi import Form
from pydantic import BaseModel, EmailStr, Field


class BaseUser(BaseModel):
    email: EmailStr


class LoginUser(BaseUser):
    password: str

    @classmethod
    def as_form(
        cls,
        username: str = Form(...),
        password: str = Form(...),
        **kwargs,
    ) -> "LoginUser":
        return cls(email=username, password=password)


class SignupUser(BaseUser):
    password1: str
    password2: str


class LoggedinUser(BaseUser):
    id: int
    role_id: int
    organization_id: Optional[int] = None


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
