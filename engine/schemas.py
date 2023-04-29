from pydantic import BaseModel


class TokenPayload(BaseModel):
    sub: str
    exp: int 
    email: str
    id: int
