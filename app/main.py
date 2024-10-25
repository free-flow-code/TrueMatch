import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager

logging.basicConfig(
        level=logging.DEBUG,
        filename='main_log.log',
        filemode='w',
        format='%(asctime)s %(levelname)s %(message)s'
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Service started")
    yield
    logging.info("Service exited")

app = FastAPI(
    title="TrueMatch",
    lifespan=lifespan,
    )
