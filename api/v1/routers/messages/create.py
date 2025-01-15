from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.services.messages import MessageService 
from db.models import Message, User
from api.utils import get_current_user

router = APIRouter(
    prefix="/create"
)

class CreateSchema(BaseModel):
    chat_id: int
    content: str 
    role: str
    file_id: int = None

@router.post('')
async def route(
    schema: CreateSchema,
    user: User = Depends(get_current_user)
):
    return await MessageService().create(
        chat_id=schema.chat_id,
        content=schema.content,
        role=schema.role,
        file_id=schema.file_id,
        user_id=user.id
    )