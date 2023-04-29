from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from engine.cleaning.schemas import CleaningRequest
from engine.dependencies import get_db
from engine.projects.models import Project

import pandas as pd
from AutoClean import AutoClean


router = APIRouter(prefix="/projects")


@router.post("/{project_id}/cleaning")
def clean_data(project_id: int, cleaning_request: CleaningRequest, db: Session = Depends(get_db)):
    project = db.query(Project).options(joinedload(Project.data_source)).where(Project.id == project_id).one()
    if project.data_source_id != cleaning_request.data_source_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Specified data source was not found in current project")

    data = pd.read_csv(project.data_source.file_path)

    for operation_set in cleaning_request.operations:
        columns = operation_set.column_subset
        config = operation_set.config

        pipeline = AutoClean(data[columns], mode="manual", **config.dict(exclude={"mode"}))
        data = pd.merge(data.convert_dtypes(), pipeline.output, how="right")

    data.to_csv(f"upload/data/cleaned_data/{project.data_source.data_source_name}.csv", index=False)

    return data.to_dict("list")
