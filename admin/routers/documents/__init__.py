from quart import Blueprint

from .get_level import router as router_get_level
from .add_category import router as router_add_category

router = Blueprint(
    name='documents_router',
    import_name='documents_router',
    url_prefix='/documents'
)

routers = [
    router_get_level,
    router_add_category
]

[router.register_blueprint(_router) for _router in routers]
