import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


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


class BaseDataSource(BaseModel):
    id: int
    data_source_name: str
    file_path: str

    class Config:
        orm_mode = True


class BaseCleaning(BaseModel):
    id: int
    # formulas: list = []

    class Config:
        orm_mode = True


class BaseFeatures(BaseModel):
    id: int
    # features: list = []

    class Config:
        orm_mode = True


class FullProject(BaseProject):
    users: list[BaseUser]
    data_source: Optional[BaseDataSource]
    cleaning: Optional[BaseCleaning]
    feature_engineering: Optional[BaseFeatures]
