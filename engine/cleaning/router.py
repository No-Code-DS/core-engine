import numpy as np
import pandas as pd
from AutoClean import AutoClean
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from engine.cleaning.models import DataCleaning, Operation
from engine.cleaning.schemas import CleaningMap, CleaningRequest
from engine.dependencies import get_current_user, get_db
from engine.projects.models import Project

NO_CODE_CUSTOM_ID = "NO_CODE_CUSTOM_ID"

router = APIRouter(prefix="/projects")


@router.get("/cleaning_map")
def cleaning_options(_=Depends(get_current_user)) -> CleaningMap:
    cleaning_map = CleaningMap()
    return cleaning_map


@router.post("/{project_id}/cleaning")
def clean_data(
    project_id: int,
    cleaning_request: CleaningRequest,
    _=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = db.query(Project).options(joinedload(Project.data_source)).where(Project.id == project_id).one()
    if project.data_source_id != cleaning_request.data_source_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specified data source was not found in current project",
        )

    cleaning = DataCleaning()
    db.add(cleaning)
    db.flush()
    project.cleaning_id = cleaning.id

    file_path = project.data_source.raw_path

    file_type = file_path.split(".")[-1]
    data = pd.read_csv(file_path)
    col_order = data.columns
    data[NO_CODE_CUSTOM_ID] = data.index + 1

    for operation_set in cleaning_request.operations:
        columns = operation_set.column_subset
        config = operation_set.config

        pipeline = AutoClean(data[[NO_CODE_CUSTOM_ID, *columns]], mode="manual", **config.dict())

        data = pd.merge(data, pipeline.output, on=NO_CODE_CUSTOM_ID, suffixes=("_x", "")).drop(
            [f"{col}_x" for col in columns], axis=1
        )

        operation = Operation(cleaning_id=cleaning.id, config=str(config.dict()), column_subset=str(columns))
        db.add(operation)

    output_path = f"upload/data/cleaned_data/{project.data_source.data_source_name}.{file_type}"
    project.data_source.clean_path = output_path

    db.commit()

    data.drop(NO_CODE_CUSTOM_ID, axis=1)
    data = data[col_order]

    data.to_csv(output_path, index=False)
    data.replace(np.nan, None, inplace=True)

    return data.to_dict("list")
