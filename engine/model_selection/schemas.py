from typing import Optional
from pydantic import BaseModel


class LinRegParamSchema(BaseModel):
    fit_intercept: Optional[bool] = True
    positive: Optional[bool] = False


class RandomForestClassSchema(BaseModel):
    n_estimators: Optional[int] = 100


class RandomForestRegSchema(BaseModel):
    n_estimators: Optional[int] = 100


modelParams = LinRegParamSchema | RandomForestRegSchema | RandomForestClassSchema


class ModelSchema(BaseModel):
    name: str
    params: modelParams
