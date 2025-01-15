from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.services.chats import ChatService
from db.models import Chat, User
from api.utils import get_current_user

router = APIRouter(
    prefix="/get_chat"
)

@router.get('')
async def route(
    id: int,
    user: User = Depends(get_current_user)
):
    return await ChatService().get_chat(
        id=id,
        user_id=user.id
    )