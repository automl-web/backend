import uuid

from dotenv import load_dotenv
from fastapi import APIRouter, UploadFile

from Dataset.Model import DatasetCreate, Dataset, DatasetUpdate
from engine import SessionDep

import shutil

import os

load_dotenv()

router = APIRouter()

@router.get("/")
def get_datasets(session: SessionDep):
    datasets = session.query(Dataset).all()
    return datasets


@router.get("/{dataset_id}")
def get_dataset(dataset_id: int, session: SessionDep):
    dataset = session.get(Dataset, dataset_id)
    return dataset


@router.post("/")
def create_dataset(dataset_create: DatasetCreate, session: SessionDep):
    dataset = Dataset.model_validate(dataset_create)
    session.add(instance=dataset)
    session.commit()
    session.refresh(dataset)
    return dataset


@router.post("/{dataset_id}/upload/")
def upload_dataset(dataset_id: int, file: UploadFile, session: SessionDep):
    dataset = session.get(Dataset, dataset_id)
    path = f"datasets/{generate_uuid()}.csv"
    output_path = f"{os.getenv("OUTPUT_PATH")}/{path}"

    with open(output_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    dataset.path = path
    session.add(instance=dataset)
    session.commit()
    session.refresh(dataset)
    return dataset


@router.patch("/{dataset_id}")
def update_dataset(dataset_id: int, dataset_update: DatasetUpdate, session: SessionDep):
    dataset = session.get(Dataset, dataset_id)
    dataset = dataset.model_validate(dataset_update)

    dataset_data = dataset_update.model_dump(exclude_unset=True)
    dataset.sqlmodel_update(dataset_data)
    session.add(instance=dataset)
    session.commit()
    session.refresh(dataset)
    return dataset


@router.delete("/{dataset_id}")
def delete_dataset(dataset_id: int, session: SessionDep):
    dataset = session.get(Dataset, dataset_id)
    session.delete(dataset)
    session.commit()
    return {"message": "Dataset deleted successfully"}


def generate_uuid():
    return str(uuid.uuid4())
