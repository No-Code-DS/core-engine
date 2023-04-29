from typing import Optional
from pydantic import BaseModel


class CleaningConfig(BaseModel):
    mode: Optional[str] = "auto"
    duplicates: Optional[str | bool] = False
    missing_num: Optional[str | bool] = False
    missing_categ: Optional[str | bool] = False
    encode_categ: Optional[list | bool] = False
    extract_datetime: Optional[str | bool] = False
    outliers: Optional[str | bool] = False
    outlier_param: Optional[int | float] = 1.5
    logfile: Optional[bool] = True
    verbose: Optional[bool] = False


class CleaningOperation(BaseModel):
    column_subset: list[str]
    config: CleaningConfig


class CleaningRequest(BaseModel):
    data_source_id: int
    operations: list[CleaningOperation]
