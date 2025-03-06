from loguru import logger
from beanie import PydanticObjectId
from quart import Blueprint, redirect, render_template, request
import os

from admin.utils import auth_required
from mongodb.services import MongoBaseService
from mongodb.models import Doc
from mongodb.database import mongo_init

router = Blueprint(
    name='documents_router_delete',
    import_name='documents_router_delete'
)

# Form for confirmation of document deletion
@router.get('/delete')
@auth_required
async def get_route():
    try:
        await mongo_init()

        document_id = request.args.get('id') 

        document = await MongoBaseService.find(
            model=Doc,
            filters={"_id": PydanticObjectId(document_id)}
        )

        children = [child.name for child in document.categories]

        return await render_template('documents/delete.html',
            id=document_id,
            name=document.name,
            children=children
        )
    except Exception as e:
        logger.error(f"Failed to delete document: {e}")
        return await render_template('error.html', error=f"Failed to delete document: {e}")

# Deleting document
@router.post('/delete')
@auth_required
async def post_route():
    try:
        await mongo_init()

        data = await request.form

        model = await MongoBaseService.find(model=Doc, filters={"_id": PydanticObjectId(data.get("id"))})

        # Removing document file
        os.remove(model.file_id) 

        await MongoBaseService.delete(model)

        return redirect('/documents/get')
    except Exception as e:
        logger.error(f"Failed to delete document: {e}")
        return await render_template('error.html', error=f"Failed to delete document: {e}")
