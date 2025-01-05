from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

from api.services.user import UserService

router = APIRouter(
    prefix="/login"
)

class AuthSchema(BaseModel):
    email: EmailStr
    password: str

@router.post('')
async def route(schema: AuthSchema):
    return await UserService().login(email=schema.email, password=schema.password)
