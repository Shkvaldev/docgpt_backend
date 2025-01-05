from fastapi import APIRouter
from api.db.database import create_tables

router = APIRouter(
    prefix="/check"
)

@router.get('')
async def route():
    #await create_tables()
    return {'status': 'ok'}
