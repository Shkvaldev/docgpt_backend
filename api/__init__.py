from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from .v1 import routers

app = FastAPI(
    title='API',
    redoc_url=None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

[app.include_router(_router) for _router in routers]

def create_app():
    # Setup config here if needed
    logger.debug('Starting API ...')
    return app
