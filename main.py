from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Dataset.Controller import router as dataset_router
from Execution.Controller import router as execution_router
# from RabbitMQListener.listener import listen
from engine import create_db_and_tables

create_db_and_tables()
#
# listen("autosklearn", get_session())
# listen("tpot", get_session())
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dataset_router, prefix="/datasets")
app.include_router(execution_router, prefix="/executions")
