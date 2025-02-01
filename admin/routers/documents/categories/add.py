from loguru import logger
from beanie import PydanticObjectId
from quart import Blueprint, jsonify, redirect, render_template, request

from admin.utils import auth_required, split_form_field
from mongodb.services import CategoryService
from mongodb.models import Category
from mongodb.database import mongo_init

router = Blueprint(
    name='categories_router_add',
    import_name='categories_router_add'
)


# Form for creating category
@router.get('/add')
@auth_required
async def get_route():
    # Handling optional form-building params 
    depth = request.args.get('depth')
    parents = request.args.get('parents')
    children = request.args.get('children')
    docs = request.args.get('docs')
    return await render_template('documents/categories/add.html',
        depth=depth,
        parents=parents,
        children=children,
        docs=docs
    )

# Processing adding category
@router.post('/add')
@auth_required
async def post_route():
    try:
        await mongo_init()

        data = await request.form
        
        await CategoryService().create(
            name=data.get("name"),
            description=data.get("description"),
            depth=int(data.get("depth")),
            parents_ids=split_form_field(data.get("parents")) or [],
            children_ids=split_form_field(data.get("children")) or [],
            docs_ids=split_form_field(data.get("docs")) or []
        ) 
        
        return redirect(f'/documents/categories/levels/{data.get("depth")}/get')
    except Exception as e:
        logger.error(f"Failed to add category: {e}")
        return await render_template('error.html', error=f"Failed to add category: {e}")
