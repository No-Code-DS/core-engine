import numpy as np
import pandas as pd
from AutoClean import AutoClean
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from engine.cleaning.models import DataCleaning, Formula
from engine.cleaning.schemas import CleaningMap, CleaningRequest
from engine.dependencies import get_current_user, get_db
from engine.projects.models import Project

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

    data = pd.read_csv(project.data_source.file_path)
    for operation_set in cleaning_request.operations:
        columns = operation_set.column_subset
        config = operation_set.config

        pipeline = AutoClean(data[columns], mode="manual", **config.dict())
        data = pd.merge(data.convert_dtypes(), pipeline.output, how="outer")

        formula = Formula(
            cleaning_id=cleaning.id, formula_string=str(config.dict()), target_column=str(columns)
        )
        db.add(formula)
    db.commit()

    data.to_csv(f"upload/data/cleaned_data/{project.data_source.data_source_name}.csv", index=False)
    data.replace(np.nan, None, inplace=True)

    return data.to_dict("list")
