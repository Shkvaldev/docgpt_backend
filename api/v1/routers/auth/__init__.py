from fastapi import APIRouter

from .login import router as router_login
from .register import router as router_register

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

routers = [router_login, router_register]
[router.include_router(_router) for _router in routers]
