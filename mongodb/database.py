from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from mongodb.models import Category, Doc
from config import settings

MONGODB_MODELS=[Category, Doc]

async def mongo_init():
    client = AsyncIOMotorClient(settings.get_mongo_uri())
    # Using postgres db name
    project = settings.postgres_db
    await init_beanie(database=client[project], document_models=MONGODB_MODELS)
