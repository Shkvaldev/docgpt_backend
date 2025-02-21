from fastapi import APIRouter
from fastapi_sso.sso.google import GoogleSSO
from config import settings

router = APIRouter(
    prefix="/google_login"
)

sso = GoogleSSO(
    client_id=settings.client_id,
    client_secret=settings.client_secret,
    redirect_uri="http://localhost:5000/auth/callback",
    allow_insecure_http=True,
)


@router.get("")
async def auth_google_init():
    """Initialize auth and redirect"""
    async with sso:
        return await sso.get_login_redirect(params={"prompt": "consent", "access_type": "offline"})