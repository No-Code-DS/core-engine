import json
from typing import Any

import numpy as np
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from engine.dependencies import get_current_user, get_db
from engine.feature_engineering.fe import magic_fe
from engine.feature_engineering.models import Feature, FeatureEngineering
from engine.feature_engineering.schema import FeRequest
from engine.projects.models import Project

router = APIRouter(prefix="/projects")


@router.post("/{project_id}/fe")
def add_features(
    project_id: int, fe_request: list[FeRequest], _=Depends(get_current_user), db: Session = Depends(get_db)
) -> dict[str, Any]:
    project = db.query(Project).options(joinedload(Project.data_source)).get(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail=f"Project with id {project_id} was not found")

    fe = FeatureEngineering()
    db.add(fe)
    db.flush()
    project.feature_engineering_id = fe.id

    file_path = project.data_source.clean_path
    data = pd.read_csv(file_path)

    for fe_config in fe_request:
        expression = {
            "left": fe_config.left,
            "operation": fe_config.operation_symbol,
            "right": fe_config.right,
        }
        feature = Feature(
            name=fe_config.name,
            feature_expression=json.dumps(expression),
            feature_engineering_id=fe.id,
        )
        db.add(feature)

        data = magic_fe(data, fe_config)

    ready_path = f"upload/data/ready/{project.data_source.data_source_name}.csv"
    data.to_csv(ready_path, index=False)
    project.data_source.ready_path = ready_path

    db.commit()

    data.replace(np.nan, None, inplace=True)
    return data.to_dict("list")
