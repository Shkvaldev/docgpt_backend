from quart import Blueprint, request, render_template, redirect
from loguru import logger
import os
import aiofiles

from admin.utils import auth_required
from mongodb.services import MongoBaseService, DocService
from mongodb.models import Doc
from mongodb.database import mongo_init
from config import settings

router = Blueprint(
    name='documents_router_create',
    import_name='documents_router_create'
)

@router.get('/add')
@auth_required
async def get_route():
    return await render_template('documents/add.html')

@router.post('/add')
@auth_required
async def post_route():
    try:
        await mongo_init()

        data = await request.form
        files = await request.files

        # Checking file presence
        if "document" not in files:
            return await render_template('error.html', error="You must attach file!")

        # Saving file
        if data.get("filename"):
            file_path = f"{settings.upload_dir}/{data.get("filename")}"
        else:
            file_name = files["document"].filename
            file_path = f"{settings.upload_dir}/{file_name}"

        await files["document"].save(file_path)

        # Creating document
        await DocService().create(
            name=data.get("name"),
            description=data.get("description"),
            file_path=file_path
        )

        return redirect('/documents/get')
    except Exception as e:
        logger.error(f"Failed to add document: {e}")
        return await render_template('error.html', error=f"Failed to add document: {e}")
