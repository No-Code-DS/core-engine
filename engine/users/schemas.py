from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    email: EmailStr

class LoginUser(BaseUser):
    password: str


class SignupUser(BaseUser):
    password1: str
    password2: str
