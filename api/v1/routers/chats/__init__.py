from fastapi import APIRouter

from .create import router as router_create
from .get_chat import router as router_get_chat
from .get_chats import router as router_get_chats
from .remove import router as router_remove


router = APIRouter(
    prefix="/chats",
    tags=["Chats"]
)

routers = [router_create, router_get_chat, router_get_chats, router_remove]
[router.include_router(_router) for _router in routers]
