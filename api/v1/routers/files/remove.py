from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.services.files import FilesService
from db.models import File_doc, User
from api.utils import get_current_user

router = APIRouter(
    prefix="/remove"
)

class RemoveSchema(BaseModel):
    id: int

@router.post('')
async def route(
    schema: RemoveSchema,
    user: User = Depends(get_current_user)
):
    return await FilesService().delete(
        id=schema.id,
        user_id=user.id
    )