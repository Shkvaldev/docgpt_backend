from fastapi import APIRouter

from .create import router as router_create
from .get_message import router as router_get_message
from .get_chat_messages import router as router_chat_messages
from .remove import router as router_remove
from .update import router as router_update

router = APIRouter(
    prefix="/messages",
    tags=["Messages"]
)

routers = [router_create, router_get_message, router_chat_messages, router_remove, router_update]
[router.include_router(_router) for _router in routers]
