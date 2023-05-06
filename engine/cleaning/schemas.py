from typing import Optional
from pydantic import BaseModel


class CleaningConfig(BaseModel):
    duplicates: Optional[str | bool] = False
    missing_num: Optional[str | bool] = False
    missing_categ: Optional[str | bool] = False
    encode_categ: Optional[list | bool] = False
    extract_datetime: Optional[str | bool] = False
    outliers: Optional[str | bool] = False
    outlier_param: Optional[int | float] = 1.5


class CleaningOperation(BaseModel):
    column_subset: list[str]
    config: CleaningConfig


class CleaningRequest(BaseModel):
    data_source_id: int
    operations: list[CleaningOperation]


class CleaningMap(BaseModel):
    # mode: list[str] = ["auto", "manual"]
    duplicates: list[str | bool] = [False, True, "auto"]
    missing_num: list[str | bool] = [False, 'auto', 'linreg', 'knn', 'mean', 'median', 'most_frequent', 'delete'] 
    missing_categ: list[str | bool] = [False, 'auto', 'logreg', 'knn', 'most_frequent', 'delete']
    encode_categ: list[str | bool | list[str]] = [False, 'auto', ['onehot'], ['label']]
    extract_datetime: list[str | bool] = [False, 'auto', 'D', 'M', 'Y', 'h', 'm', 's']
    outliers: list[str | bool] = [False, "auto", "winz", "delete"]
    # outlier_param: int | float = 1.5
    # logfile: bool = True
    # verbose: bool = False