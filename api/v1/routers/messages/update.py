from fastapi import APIRouter, Depends
from pydantic import BaseModel
from api.utils import get_current_user
from db.models import User

from api.services.messages import MessageService 
from db.models import Message

router = APIRouter(
    prefix="/update"
)

class UpdateScheme(BaseModel):
    id: int
    content: str

@router.post('')
async def route(
    schema: UpdateScheme,
    user: User = Depends(get_current_user)
):
    return await MessageService().update(
        id=schema.id,
        user_id=user.id,
        content=schema.content
        )