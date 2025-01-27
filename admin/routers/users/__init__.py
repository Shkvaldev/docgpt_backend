from quart import Blueprint

from .all import router as router_all
from .get_chats import router as router_get_chats
from .get_chat import router as router_get_chat

router = Blueprint(
    name='users_router',
    import_name='users_router',
    url_prefix='/users'
)

routers = [
    router_all,
    router_get_chats,
    router_get_chat
]

[router.register_blueprint(_router) for _router in routers]
