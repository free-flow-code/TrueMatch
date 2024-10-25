import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from app.config import settings
from app.users.router import router as router_clients
from app.images.router import router as router_images

logging.basicConfig(
        level=logging.DEBUG,
        filename='main_log.log',
        filemode='w',
        format='%(asctime)s %(levelname)s %(message)s'
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Service started")
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf8",
        decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield
    logging.info("Service exited")

app = FastAPI(
    title="TrueMatch",
    openapi_prefix="/api",
    lifespan=lifespan,
    )
app.mount("/static", StaticFiles(directory="app/static"), "static")
app.include_router(router_clients)
app.include_router(router_images)

origins = settings.ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization"],
)
