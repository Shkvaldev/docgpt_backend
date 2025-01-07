from fastapi import APIRouter
from db.database import create_tables

router = APIRouter(
    prefix="/check"
)

@router.get('')
async def route():
    #await create_tables()
    return {'status': 'ok'}
