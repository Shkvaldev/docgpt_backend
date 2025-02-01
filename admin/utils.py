from typing import List, Optional
import jwt
from functools import wraps
from loguru import logger
import aiohttp
import asyncio

from quart import session, url_for, redirect, g

from config import settings

async def check_token(token: str) -> bool:
    try:
        jwt.decode(token, settings.jwt_secret, algorithms='HS256')
        await asyncio.sleep(0)
        return True
    except jwt.InvalidSignatureError:
        return False 
    except jwt.ExpiredSignatureError:
        return False 
    except Exception:
        return False

def auth_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with g.app.app_context():
            if 'token' in session:
                if await check_token(session.get('token')):
                    return await func(*args, **kwargs)
        return redirect(url_for('login'))

    return wrapper

async def auth(email: str, password: str):
    try:
        url = f"{settings.api_link}/v1/auth/login"
        headers = {
            "Content-Type": "application/json"
        }
        auth_data = {
            "email": email,
            "password": password
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(url, json=auth_data) as response:
                if response.status != 200:
                    raise ValueError("Failed to login: maybe you are not an admin?")
                data = await response.json()
                return {
                    "id": data["id"],
                    "name": data["name"],
                    "token": data["token"]
                }
    except Exception as e:
        logger.error(f"Failed to auth: {e}")
        raise e

# Utility for splitting args from form, separated via ','
def split_form_field(data: Optional[str]) -> Optional[List[str]]:
    """
    Splits form field (str) with ',' separator.

    If no data - returns None, else - list with args
    """
    if not data:
        return

    if len(data) == 0:
        return
    
    args = [arg for arg in data.split(',') if arg != '']

    if len(args) == 0:
        return

    return args
