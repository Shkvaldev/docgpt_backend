from fastapi import APIRouter

from .routers.health import router as router_health
from .routers.auth import router as router_auth
from .routers.users import router as router_users
from .routers.chats import router as router_chats
from .routers.files import router as router_files
from .routers.messages import router as router_messages

router = APIRouter(
    prefix="/v1",
    tags=["V1"]
)

routers = [router_health, router_auth, router_users, router_chats, router_files, router_messages]
[router.include_router(_router) for _router in routers]
