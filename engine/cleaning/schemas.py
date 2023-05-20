from typing import Optional

from pydantic import BaseModel


class CleaningConfig(BaseModel):
    duplicates: Optional[bool | str] = False
    missing_num: Optional[bool | str] = False
    missing_categ: Optional[bool | str] = False
    encode_categ: Optional[list | bool] = False
    extract_datetime: Optional[bool | str] = False
    outliers: Optional[bool | str] = False
    outlier_param: Optional[int | float] = 1.5


class CleaningOperation(BaseModel):
    column_subset: list[str]
    config: CleaningConfig


class CleaningRequest(BaseModel):
    data_source_id: int
    operations: list[CleaningOperation]


class CleaningMap(BaseModel):
    # mode: list[str] = ["auto", "manual"]
    duplicates: list[str | bool] = [False, "auto"]
    missing_num: list[str | bool] = [
        False,
        "auto",
        # "linreg",
        "knn",
        "mean",
        "median",
        "most_frequent",
        "delete",
    ]
    missing_categ: list[str | bool] = [False, "auto", "logreg", "knn", "most_frequent", "delete"]
    encode_categ: list[str | bool | list[str]] = [False, "auto", ["onehot"], ["label"]]
    extract_datetime: list[str | bool] = [False, "auto", "D", "M", "Y", "h", "m", "s"]
    outliers: list[str | bool] = [False, "auto", "winz", "delete"]
    # outlier_param: int | float = 1.5
    # logfile: bool = True
    # verbose: bool = False
