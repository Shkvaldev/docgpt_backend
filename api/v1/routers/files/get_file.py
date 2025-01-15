from fastapi import APIRouter, Depends
from api.services.files import FilesService
from db.models import User, File_doc
from api.utils import get_current_user

router = APIRouter(
    prefix="/get_file"
)

@router.get('')
async def route(
    id: int,
    user: User = Depends(get_current_user)
):
    return await FilesService().get_file(id=id, user_id=user.id)