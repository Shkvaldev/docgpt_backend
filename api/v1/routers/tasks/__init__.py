from fastapi import APIRouter

from .create import router as router_create 
from .get_status import router as router_get_status
from .delete import router as router_delete

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

routers = [router_create, router_get_status, router_delete]
[router.include_router(_router) for _router in routers]
