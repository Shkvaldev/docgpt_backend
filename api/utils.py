import jwt
from typing import Annotated
from datetime import datetime, timezone, timedelta
import smtplib
from email.message import EmailMessage
from loguru import logger
import uuid
import os

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from db.models import User
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

def send_verification_code(email, otp: str):
    """
    Отправка одноразового кода по почте
    """
    msg = EmailMessage()
    msg["Subject"] = 'Код подтверждения в DocGPT'
    msg['From'] = settings.email_address
    msg['To'] = email
    msg.set_content(f"Ваш код подтверждения: {otp}")
    
    try:
        server = smtplib.SMTP(settings.email_server)
        server.starttls()
        server.login(settings.email_address, settings.email_password)
        server.send_message(msg)
        server.quit()
        logger.debug(f"Verification for `{email}` is sent")
    except Exception as e:
        logger.error(f"Failed to send verifiaction code to `{email}`: {e}")

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

def generate_unique_filename(original_filename: str) -> str:
    """
    Генерирует уникальное имя файла, сохраняя оригинальное расширение
    """
    # Получаем расширение оригинального файла
    _, extension = os.path.splitext(original_filename)
    
    # Генерируем уникальное имя и добавляем расширение
    return f"{uuid.uuid4()}{extension}"
