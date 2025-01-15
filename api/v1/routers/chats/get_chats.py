from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from api.services.chats import ChatService
from db.models import Chat, User
from api.utils import get_current_user

router = APIRouter(
    prefix="/get_chats"
)

@router.get('')
async def route(user: User = Depends(get_current_user)):
    return await ChatService().get_chats(user_id=user.id)