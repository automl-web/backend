from sqlmodel import SQLModel, Field, Relationship

from Execution.Model import Execution


class DatasetBase(SQLModel):
    description: str | None = Field(default=None)
    version: int | None = Field(default=1)
    name: str | None = Field(default=None)
    file_size: int | None = Field(default=None)
    file_format: str | None = Field(default=None)
    date_created: str | None = Field(default=None)
    author: str | None = Field(default=None)
    target_feature: str | None = Field(default=None)


class Dataset(DatasetBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    path: str | None = Field(default=None)

    executions: list["Execution"] = Relationship(back_populates="dataset")


class DatasetCreate(DatasetBase):
    pass


class DatasetUpdate(DatasetBase):
    description: str | None = None
    version: int | None = None
    name: str | None = None
    file_size: int | None = None
    file_format: str | None = None
    date_created: str | None = None
    author: str | None = None
