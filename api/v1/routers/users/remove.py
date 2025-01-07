from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from loguru import logger

from api.services.base import BaseService
from db.models import User
from api.utils import get_current_user

router = APIRouter(
    prefix="/remove"
)

class RemoveSchema(BaseModel):
    email: EmailStr

@router.post('')
async def route(schema: RemoveSchema, user: User = Depends(get_current_user)):
    try:
        await BaseService().delete(User, user.id)
    except Exception as e:
        logger.error(f"Failed to delete `{schema.email}` user: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to delete due to server error"
        )
    return {
        'status': 'ok'
    }
