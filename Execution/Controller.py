import json
import uuid

from fastapi import APIRouter

from Execution.Model import Execution, ExecutionUpdate, ExecutionCreate
from engine import SessionDep

import pika

import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

@router.get("/")
def get_datasets(session: SessionDep):
    executions = session.query(Execution).all()
    return executions


@router.get("/{execution_id}")
def get_dataset(execution_id: int, session: SessionDep):
    execution = session.get(Execution, execution_id)
    return execution


@router.post("/")
def create_dataset(execution_create: ExecutionCreate, session: SessionDep):
    execution = Execution.model_validate(execution_create)
    execution.storage_id = f"{generate_uuid()}"
    session.add(instance=execution)
    session.commit()
    session.refresh(execution)

    os.makedirs(f"{os.getenv("OUTPUT_PATH")}/{execution.storage_id}")
    return execution


@router.patch("/{execution_id}")
def update_dataset(execution_id: int, execution_update: ExecutionUpdate, session: SessionDep):
    execution = session.get(Execution, execution_id)
    execution = execution.model_validate(execution_update)

    execution_data = execution_update.model_dump(exclude_unset=True)
    execution.sqlmodel_update(execution_data)
    session.add(instance=execution)
    session.commit()
    session.refresh(execution)
    return execution


@router.delete("/{execution_id}")
def delete_dataset(execution_id: int, session: SessionDep):
    execution = session.get(Execution, execution_id)
    session.delete(execution)
    session.commit()
    return {"message": "Execution deleted successfully"}


@router.post("/{execution_id}/run/")
def run(execution_id: int, session: SessionDep):
    execution = session.get(Execution, execution_id)
    data = execution.dict()
    data["dataset"] = execution.dataset.dict()
    data = json.dumps(data)
    print(data)

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=execution.type)
    channel.basic_publish(exchange='', routing_key=execution.type, body=data)
    connection.close()

def generate_uuid():
    return str(uuid.uuid4())