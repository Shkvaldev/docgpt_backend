from fastapi import APIRouter, Request
from fastapi_sso.sso.google import GoogleSSO
from config import Settings

router = APIRouter(
    prefix="/google_callback"
)

sso = GoogleSSO(
    client_id=Settings.client_id,
    client_secret=Settings.client_secret,
    redirect_uri="http://localhost:5000/auth/callback",
    allow_insecure_http=True,
)

@router.get("")
async def auth_callback(request: Request):
    """Verify login"""
    async with sso:
        user = await sso.verify_and_process(request)
    return user