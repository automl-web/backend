from fastapi import FastAPI

from Dataset.Controller import router as dataset_router
from Execution.Controller import router as execution_router
# from RabbitMQListener.listener import listen
from engine import create_db_and_tables, get_session

create_db_and_tables()
#
# listen("autosklearn", get_session())
# listen("tpot", get_session())
app = FastAPI()
app.include_router(dataset_router, prefix="/dataset")
app.include_router(execution_router, prefix="/execution")
