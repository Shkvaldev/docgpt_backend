from fastapi import APIRouter

from .login import router as router_login
from .register import router as router_register
from .verify_code import router as router_verify_code

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

routers = [router_login, router_register, router_verify_code]
[router.include_router(_router) for _router in routers]
