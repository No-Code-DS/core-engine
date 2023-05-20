from fastapi import APIRouter
import json
import pika

from engine.model_selection.schemas import ModelSchema


router = APIRouter(prefix="/projects")


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
