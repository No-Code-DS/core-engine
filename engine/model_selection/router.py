from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from engine.dependencies import get_current_user, get_db
from engine.model_selection.models import SelectedModel
from engine.model_selection.schemas import ModelConfigSchema, ModelSchema
from engine.projects.models import Project

router = APIRouter(prefix="/projects")


@router.get("/model_map")
def get_model_map() -> list[ModelConfigSchema]:
    """returns possible models and their parameters"""
    models = [
        ModelConfigSchema(
            name="LinearRegression",
            params=[{"name": "fit_intercept", "type": "bool"}, {"name": "positive", "type": "bool"}],
        ),
        ModelConfigSchema(name="RandomForestClassifier", params=[{"name": "n_estimators", "type": "int"}]),
        ModelConfigSchema(name="RandomForestRegressor", params=[{"name": "n_estimators", "type": "int"}]),
    ]
    return models


@router.post("/{project_id}/model")
def select_model(project_id: int, model_config: ModelSchema, db: Session = Depends(get_db)):
    project = db.query(Project).get(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail=f"Project with id {project_id} was not found")


    model = SelectedModel(
        model_name=model_config.name,
        prediction_field=model_config.prediction_field,
        config=model_config.params,
    )
    db.add(model)
    db.flush()

    db.commit()

    return {"status": "Training"}


@router.get("/{project_id}/model")
def get_training_status(project_id: int, _=Depends(get_current_user), db: Session = Depends(get_db)):
    project = db.query(Project).get(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail=f"Project with id {project_id} was not found")

    if project.data_source_id is None:
        status = "Empty"
    elif project.cleaning_id is None:
        status = "Empty"
    elif project.feature_engineering_id is None:
        status = "Cleaning"
    elif project.model_id is None:
        status = "FE"
    elif project.model_id is not None:
        status = project.model.status

    return {"status": status}
