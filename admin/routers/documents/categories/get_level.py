from quart import Blueprint, render_template
from loguru import logger

from admin.utils import auth_required
from mongodb.services import MongoBaseService
from mongodb.models import Category
from mongodb.database import mongo_init

router = Blueprint(
    name='categories_router_get_level',
    import_name='categories_router_get_level'
)

# Show documents of default level (depth = 0) 
@router.get('/levels/get')
@auth_required
async def default_route():
    try:
        await mongo_init()

        categories = await MongoBaseService.find_all(
            model=Category,
            filters={'depth': 0}
        )
    except Exception as e:
        categories = []
    return await render_template('documents/categories/get_level.html', 
         categories=categories
    )

# Show documents of the same level 
@router.get('/levels/<depth>/get')
@auth_required
async def per_depth_route(depth):
    try:
        await mongo_init()

        categories = await MongoBaseService.find_all(
            model=Category,
            filters={'depth': int(depth)}
        )
    except Exception as e:
        categories = []
    return await render_template('documents/categories/get_level.html',
        categories=categories
    )
