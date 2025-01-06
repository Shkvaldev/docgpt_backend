from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

from api.services.user import UserService

router = APIRouter(
    prefix="/verify_code"
)

class VerifySchema(BaseModel):
    email: EmailStr
    code: str

@router.post('')
async def route(schema: VerifySchema):
    return await UserService().verify_code(email=schema.email, code=schema.code)
