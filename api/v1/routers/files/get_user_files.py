from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.services.files import FilesService
from db.models import File_doc, User
from api.utils import get_current_user

router = APIRouter(
    prefix="/get_user_files"
)

@router.get('')
async def route(user: User = Depends(get_current_user)):
    return await FilesService().get_files(user_id=user.id)