from pydantic import BaseModel


class FeRequest(BaseModel):
    left: str
    right: str
    operation_symbol: str
    name: str
