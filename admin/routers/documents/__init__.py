from quart import Blueprint

from .categories import router as router_categories

router = Blueprint(
    name='documents_router',
    import_name='documents_router',
    url_prefix='/documents'
)

routers = [
    router_categories
]

[router.register_blueprint(_router) for _router in routers]
