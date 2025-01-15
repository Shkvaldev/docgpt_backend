from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.services.chats import ChatService
from db.models import Chat, User
from api.utils import get_current_user

router = APIRouter(
    prefix="/remove"
)

class RemoveSchema(BaseModel):
    id: int

@router.post('')
async def route(
    scheme: RemoveSchema,
    user: User = Depends(get_current_user)
):
    return await ChatService().delete(id=scheme.id, user_id=user.id)