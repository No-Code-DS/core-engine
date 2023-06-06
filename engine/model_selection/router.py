import json
import os

import pika
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from engine.dependencies import get_current_user, get_db
from engine.model_selection.models import SelectedModel, StatusEnum
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

    # put rabbitmq event with file and model config
    connection = pika.BlockingConnection(pika.ConnectionParameters(os.environ["RABBIT_URL"]))
    channel = connection.channel()

    model = SelectedModel(
        model_name=model_config.name,
        prediction_field=model_config.prediction_field,
        config=str(model_config.params.dict()),
        status=StatusEnum.TRAINING,
    )
    db.add(model)
    db.flush()

    project.model_id = model.id

    db.commit()

    properties = pika.BasicProperties("training_start")
    channel.basic_publish(
        exchange="",
        routing_key="training",
        body=json.dumps(
            {"model_id": model.id, "file_path": project.data_source.ready_path, **model_config.dict()}
        ),
        properties=properties,
    )
    connection.close()

    return {"status": "Training"}


@router.get("/{project_id}/model")
def get_training_status(project_id: int, _=Depends(get_current_user), db: Session = Depends(get_db)):
    project = db.query(Project).get(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail=f"Project with id {project_id} was not found")

    metrics = None
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
        if project.model.status == StatusEnum.TRAINED:
            metrics = json.loads(project.model.evaluation)

    return {"status": status, "metrics": metrics}
