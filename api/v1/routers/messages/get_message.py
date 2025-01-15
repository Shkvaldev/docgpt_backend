from fastapi import APIRouter, Depends


from api.services.messages import MessageService 
from db.models import Message, User
from api.utils import get_current_user

router = APIRouter(
    prefix="/get_message"
)


@router.get('')
async def route(
    id: int,
    user: User = Depends(get_current_user)
):
    return await MessageService().get_message(id=id, user_id=user.id)