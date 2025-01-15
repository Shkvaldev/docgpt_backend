from fastapi import APIRouter, File, UploadFile, Form, Depends
from api.services.files import FilesService
from api.utils import generate_unique_filename
from db.models import User
from api.utils import get_current_user

router = APIRouter(
    prefix="/create"
)

@router.post('')
async def route(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user)
):
    unique_filename = generate_unique_filename(file.filename)
    return await FilesService().create(
        path=f"files/{unique_filename}",
        file=file,
        user_id=user.id
    )