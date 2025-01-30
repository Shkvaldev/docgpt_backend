from quart import Blueprint, render_template

from admin.utils import auth_required
from mongodb.services import MongoBaseService
from mongodb.models import Category

router = Blueprint(
    name='documents_router_add_category',
    import_name='documents_router_add_category'
)

# Form for creating category
@router.get('/categories/add')
@auth_required
async def get_route():
    # TODO: implement autofilling using request parameters
    return await render_template('documents/add_category.html')

# Processing adding category
@router.post('/categories/add')
@auth_required
async def post_route():
    pass
