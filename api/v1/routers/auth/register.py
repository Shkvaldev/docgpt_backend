from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

from api.services.user import UserService

router = APIRouter(
    prefix="/register"
)

class RegisterSchema(BaseModel):
    name: str
    email: EmailStr
    password: str

@router.post('')
async def route(schema: RegisterSchema):
    return await UserService().create(name=schema.name, email=schema.email, password=schema.password)
