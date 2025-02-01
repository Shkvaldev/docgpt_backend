from quart import Blueprint

from .get_level import router as router_get_level
from .add import router as router_add_category
from .delete import router as router_delete_category 

router = Blueprint(
    name='categories_router',
    import_name='categories_router',
    url_prefix='/categories'
)

routers = [
    router_get_level,
    router_add_category,
    router_delete_category
]

[router.register_blueprint(_router) for _router in routers]
