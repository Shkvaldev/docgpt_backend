from fastapi import APIRouter, Depends
from api.utils import get_current_user
from db.models import User

from api.services.messages import MessageService
from db.models import Message

router = APIRouter(
    prefix="/get_chat_messages"
)

@router.get('')
async def route(
    chat_id: int, 
    user: User = Depends(get_current_user
)):
    return await MessageService().get_messages(chat_id=chat_id, user_id=user.id)