from quart import Blueprint

from .categories import router as router_categories
from .get_all import router as router_get_all
from .add import router as router_add
from .delete import router as router_delete

router = Blueprint(
    name='documents_router',
    import_name='documents_router',
    url_prefix='/documents'
)

routers = [
    router_categories,
    router_get_all,
    router_add,
    router_delete
]

[router.register_blueprint(_router) for _router in routers]
