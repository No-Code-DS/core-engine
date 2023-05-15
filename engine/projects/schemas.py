import ast
import datetime
from typing import Any, Optional

from pydantic import BaseModel, EmailStr, validator


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


class BaseFormula(BaseModel):
    id: int
    formula_string: dict[str, Any]
    target_column: list[str]

    @validator("formula_string", "target_column", pre=True)
    def eval_fields(cls, v):
        return ast.literal_eval(v)

    class Config:
        orm_mode = True


class BaseCleaning(BaseModel):
    id: int
    formulas: list[BaseFormula] = []

    class Config:
        orm_mode = True


class BaseFeature(BaseModel):
    id: int
    feature_name: str
    feature_expression: str

    class Config:
        orm_mode = True


class BaseFeatures(BaseModel):
    id: int
    features: list[BaseFeature]

    class Config:
        orm_mode = True


class FullProject(BaseProject):
    users: list[BaseUser]
    data_source: Optional[BaseDataSource]
    cleaning: Optional[BaseCleaning]
    feature_engineering: Optional[BaseFeatures]
