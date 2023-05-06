from typing import Any
from fastapi import APIRouter, Depends, HTTPException
import numpy as np
import pandas as pd
from sqlalchemy.orm import Session, joinedload

from engine.dependencies import get_current_user, get_db
from engine.feature_engineering.fe import magic_fe
from engine.feature_engineering.models import Feature, FeatureEngineering
from engine.feature_engineering.schema import FeRequest
from engine.projects.models import Project


router = APIRouter(prefix="/projects")


@router.post("/{project_id}/fe")
def add_features(
    project_id: int, 
    fe_request: list[FeRequest], 
    _ = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    project = db.query(Project).options(joinedload(Project.data_source)).get(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail=f"Project with id {project_id} was not found")

    fe = FeatureEngineering()
    db.add(fe)
    db.flush()
    project.feature_engineering_id = fe.id
    for fe_config in fe_request:
        feature = Feature(
            feature_name = fe_config.name, 
            feature_expression = f"{fe_config.left} {fe_config.operation_symbol} {fe_config.right}",
            feature_engineering_id = fe.id
        )
        db.add(feature)

        data = pd.read_csv(project.data_source.file_path)
        data = magic_fe(data, fe_config)
        data.to_csv(f"upload/data/ready/{project.data_source.data_source_name}.csv", index=False)

    db.commit()

    data.replace(np.nan, None, inplace=True)
    return data.to_dict("list")
