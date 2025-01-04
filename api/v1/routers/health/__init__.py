from fastapi import APIRouter

from .check import router as router_check

router = APIRouter(
    prefix="/health",
    tags=["Service"]
)

routers = [router_check]
[router.include_router(_router) for _router in routers]
