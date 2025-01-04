from fastapi import APIRouter

router = APIRouter(
    prefix="/check"
)

@router.get('')
async def route():
    return {'status': 'ok'}
