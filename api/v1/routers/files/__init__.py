from fastapi import APIRouter

from .create import router as router_create
from .get_file import router as router_get_file
from .get_user_files import router as router_user_files
from .remove import router as router_remove

router = APIRouter(
    prefix="/files",
    tags=["Files"]
)

routers = [router_create, router_get_file, router_user_files, router_remove]
[router.include_router(_router) for _router in routers]
