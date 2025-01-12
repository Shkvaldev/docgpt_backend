from flask import Blueprint

from .all import router as router_all

router = Blueprint(
    name='users_router',
    import_name='users_router',
    url_prefix='/users'
)

routers = [
    router_all
]

[router.register_blueprint(_router) for _router in routers]
