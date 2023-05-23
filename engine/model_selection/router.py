from typing import Any
from fastapi import APIRouter
import json
import pika

from engine.model_selection.schemas import ModelConfigSchema, ModelSchema


router = APIRouter(prefix="/projects")


@router.get("/model_map")
def get_model_map() -> list[ModelConfigSchema]:
    """returns possible models and their parameters"""
    models = [
        ModelConfigSchema(name="LinearRegression", params=[{"name": "fit_intercept", "type": "bool"}, {"name": "positive", "type": "bool"}]),
        ModelConfigSchema(name="RandomForestClassifier", params=[{"name": "n_estimators", "type": "int"}]),
        ModelConfigSchema(name="RandomForestRegressor", params=[{"name": "n_estimators", "type": "int"}]),
    ]
    return models


@router.post("/{project_id}/model")
def select_model(model_config: ModelSchema) -> None:
    # put rabbitmq event with file and model config
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    properties = pika.BasicProperties("training_start")
    channel.basic_publish(
        exchange='',
        routing_key='training',
        body=json.dumps({"model": "LinearRegression", "fit_intercept": True, "positive": False}),
        properties=properties
    )
    print("published from engine")
    connection.close()
