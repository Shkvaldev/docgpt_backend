from fastapi import APIRouter

from .web_socket import router as router_web_socket

router = APIRouter(
    prefix="/web_sockets",
    tags=["web_sockets"]
)

routers = [router_web_socket]
[router.include_router(_router) for _router in routers]
