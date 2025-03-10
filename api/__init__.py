import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from loguru import logger
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .v1 import router as router_v1
from mongodb.database import mongo_init
from rabbitmq import create_queues, update_tasks_status

# Lifespan defining
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Init mongodb
    await mongo_init()
    # Autocreate needed rabbitmq queues
    await create_queues()
    # Create auto tasks's statuses updater
    scheduler = AsyncIOScheduler()
    scheduler.add_job(update_tasks_status, "interval", seconds=3)
    scheduler.start()

    yield

app = FastAPI(
    title='DocGPT API',
    redoc_url=None,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/files", StaticFiles(directory="static", html=True), name="static")


routers = [router_v1]
[app.include_router(_router) for _router in routers]

def create_app():
    logger.debug('Starting API ...')
    return app
