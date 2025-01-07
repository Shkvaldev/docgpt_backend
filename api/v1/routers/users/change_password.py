from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.services.user import UserService
from db.models import User
from api.utils import get_current_user

router = APIRouter(
    prefix="/change_password"
)

class ChangePasswordSchema(BaseModel):
    new_password: str

@router.post('')
async def route(schema: ChangePasswordSchema, user: User = Depends(get_current_user)):
    return await UserService().change_password(user=user, new_password=schema.new_password)
