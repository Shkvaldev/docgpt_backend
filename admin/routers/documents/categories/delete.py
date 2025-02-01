from loguru import logger
from beanie import PydanticObjectId
from quart import Blueprint, redirect, render_template, request

from admin.utils import auth_required, split_form_field
from mongodb.services import MongoBaseService, CategoryService
from mongodb.models import Category
from mongodb.database import mongo_init

router = Blueprint(
    name='categories_router_delete',
    import_name='categories_router_delete'
)

# Form for confirmation of category deletion
@router.get('/delete')
@auth_required
async def get_route():
    try:
        await mongo_init()

        category_id = request.args.get('id') 

        category = await MongoBaseService.find(
            model=Category,
            filters={"_id": PydanticObjectId(category_id)}
        )

        children = [child.name for child in category.children]

        return await render_template('documents/categories/delete.html',
            id=category_id,
            children=children
        )
    except Exception as e:
        logger.error(f"Failed to delete category: {e}")
        return await render_template('error.html', error=f"Failed to delete category: {e}")

# Deleting category
@router.post('/delete')
@auth_required
async def post_route():
    try:
        await mongo_init()

        data = await request.form

        model = await MongoBaseService.find(model=Category, filters={"_id": PydanticObjectId(data.get("id"))})
        await MongoBaseService.delete(model)

        return redirect('/documents/categories/levels/get')
    except Exception as e:
        logger.error(f"Failed to delete category: {e}")
        return await render_template('error.html', error=f"Failed to delete category: {e}")
