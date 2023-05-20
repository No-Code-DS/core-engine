from fastapi import APIRouter
import pika

from engine.model_selection.schemas import ModelSchema


router = APIRouter(prefix="/projects")


@router.post("/{project_id}/model")
def select_model(model_config: ModelSchema) -> None:
    # put rabbitmq event with file and model config
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='training')
    channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='hello world!!!')
    print("[x] Sent 'Hello World!'")
    connection.close()
