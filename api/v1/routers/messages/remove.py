from fastapi import APIRouter, Depends
from pydantic import BaseModel
from api.utils import get_current_user
from db.models import User

from api.services.messages import MessageService 
from db.models import Message

router = APIRouter(
    prefix="/remove"
)

class RemoveScheme(BaseModel):
    id: int

@router.post('')
async def route(
    schema: RemoveScheme,
    user: User = Depends(get_current_user)
):
    return await MessageService().delete(
        id=schema.id,
        user_id=user.id
    )