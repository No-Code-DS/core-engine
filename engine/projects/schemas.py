import ast
import datetime
from typing import Any, Optional

from pydantic import BaseModel, EmailStr, Field, root_validator, validator


class BaseProject(BaseModel):
    id: int
    project_name: str
    description: str
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class ProjectCreate(BaseModel):
    project_name: str
    description: str


class BaseUser(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class BaseDataSource(BaseModel):
    id: int
    data_source_name: str
    raw_path: str
    clean_path: Optional[str] = None
    ready_path: Optional[str] = None

    class Config:
        orm_mode = True


class BaseOperation(BaseModel):
    config: dict[str, Any]
    column_subset: list[str]

    @validator("config", "column_subset", pre=True)
    def eval_fields(cls, v):
        return ast.literal_eval(v)

    class Config:
        orm_mode = True


class BaseCleaning(BaseModel):
    id: int
    operations: list[BaseOperation] = []

    class Config:
        orm_mode = True


class BaseFeature(BaseModel):
    name: str
    feature_expression: str = Field(exclude=True)
    left: Optional[str]
    right: Optional[str]
    operation_symbol: Optional[str]

    @root_validator
    def eval_expr(cls, values):
        conf = ast.literal_eval(values["feature_expression"])
        values["left"] = conf["left"]
        values["right"] = conf["right"]
        values["operation_symbol"] = conf["operation"]
        return values

    class Config:
        orm_mode = True


class BaseFeatures(BaseModel):
    id: int
    features: list[BaseFeature]

    class Config:
        orm_mode = True


class BaseSelectedModel(BaseModel):
    model_name: str
    prediction_field: str
    status: Optional[str] = None
    config: Optional[dict[str, Any]] = None
    evaluation: Optional[dict[str, int]] = None

    @validator("config", "evaluation", pre=True)
    def eval_fields(cls, v):
        return ast.literal_eval(v) if v is not None else None

    @validator("status", pre=True)
    def eval_status(cls, v):
        return v.value if v is not None else None

    class Config:
        orm_mode = True


class FullProject(BaseProject):
    users: list[BaseUser]
    data_source: Optional[BaseDataSource]
    cleaning: Optional[BaseCleaning]
    feature_engineering: Optional[BaseFeatures]
    model: Optional[BaseSelectedModel]
    status: str = "Empty"

    @root_validator
    def eval_expr(cls, values):
        if values["data_source"] is None:
            values["status"] = "Empty"
        elif values["cleaning"] is None:
            values["status"] = "Empty"
        elif values["feature_engineering"] is None:
            values["status"] = "Cleaning"
        elif values["model"] is None:
            values["status"] = "FE"
        elif values["model"] is not None:
            values["status"] = values["model"].status
        return values
