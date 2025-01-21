import jwt
from functools import wraps
from loguru import logger
import requests

from quart import session, url_for, redirect, g

from config import settings

def check_token(token: str) -> bool:
    try:
        jwt.decode(token, settings.jwt_secret, algorithms='HS256')
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
                if check_token(session.get('token')):
                    return await func(*args, **kwargs)
        return redirect(url_for('login'))

    return wrapper

def auth(email: str, password: str):
    try:
        url = f"{settings.api_link}/v1/auth/login"
        headers = {
            "Content-Type": "application/json"
        }
        auth_data = {
            "email": email,
            "password": password
        }
        response = requests.post(url=url, headers=headers, json=auth_data)
        if response.status_code != 200:
            raise ValueError("Failed to login: maybe you are not an admin?")
        data = response.json()
        return {
            "id": data["id"],
            "name": data["name"],
            "token": data["token"]
        }
    except Exception as e:
        logger.error(f"Failed to auth: {e}")
        raise e
