from fastapi import APIRouter

from .remove import router as router_remove
from .change_password import router as router_change_password

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

routers = [router_remove, router_change_password]
[router.include_router(_router) for _router in routers]
