from typing import Optional
from pydantic import BaseModel

from engine.types import Params


class LinRegConfigSchema(BaseModel):
    fit_intercept: Optional[bool] = True
    positive: Optional[bool] = False


class RandomForestClassConfigSchema(BaseModel):
    n_estimators: Optional[int] = 100


class RandomForestRegConfigSchema(BaseModel):
    n_estimators: Optional[int] = 100


modelParams = LinRegConfigSchema | RandomForestRegConfigSchema | RandomForestClassConfigSchema


class ModelSchema(BaseModel):
    name: str
    params: modelParams


class ModelConfigSchema(BaseModel):
    name: str
    params: list[Params]
