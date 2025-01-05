import jwt
from typing import Annotated
from datetime import datetime, timezone, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from api.db.models import User
from api.services.base import BaseService
from config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")

def generate_token(email: str) -> str:
    """
    Генерация токена авторизации
    """
    return jwt.encode(
        {
            "email": email,
            "exp": datetime.now(tz=timezone.utc) + timedelta(days=7)
        },
        settings.jwt_secret,
        algorithm="HS256",
    )

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Возвращает пользователя по токену
    """
    try:
        data = jwt.decode(token, settings.jwt_secret, algorithms='HS256')
        user = await BaseService().get(User, email=data['email'])
        if not user:
            raise HTTPException(
                status_code=403,
                detail='Detected jwt violation',
            )
        return user
    except jwt.InvalidSignatureError:
        raise HTTPException(
            status_code=403,
            detail='Invalid token',
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=403,
            detail='Token expired',
        )
    except Exception:
        raise HTTPException(
            status_code=403,
            detail='Invalid token',
        )

