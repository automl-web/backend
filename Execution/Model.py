from typing import Optional

from sqlmodel import SQLModel, Field, Relationship



class ExecutionBase(SQLModel):
    name: str = Field(default=None)
    description: str | None = Field(default=None)
    type: str | None = Field(default=None)
    dataset_id: int | None = Field(default=None, foreign_key="dataset.id")

class Execution(ExecutionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    score: float | None = Field(default=None)
    storage_id: str = Field(default=None)

    dataset: Optional["Dataset"] = Relationship(back_populates="executions")


class ExecutionCreate(ExecutionBase):
    pass


class ExecutionUpdate(ExecutionBase):
    name: str | None = None
    description: str | None = None
    type: str | None = None
