from fastapi import APIRouter

from .routers.health import router as router_health
from .routers.auth import router as router_auth
from .routers.users import router as router_users

router = APIRouter(
    prefix="/v1",
    tags=["V1"]
)

routers = [router_health, router_auth, router_users]
[router.include_router(_router) for _router in routers]
