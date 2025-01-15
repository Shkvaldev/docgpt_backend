from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.services.chats import ChatService
from db.models import Chat, User
from api.utils import get_current_user

router = APIRouter(
    prefix="/create"
)

@router.post('')
async def route(user: User = Depends(get_current_user)):
    return await ChatService().create(user_id=user.id)
