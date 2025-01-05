from datetime import datetime
from passlib.hash import pbkdf2_sha512
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr

from api.services.base import BaseService
from api.db.models import User
from api.utils import generate_token
from config import settings



class UserService:
    """
    Пользовательский CRUD+ менеджер
    """
    def __init__(self):
        self.model = User

    @staticmethod
    async def generate_user_dict(user: User) -> dict:
        """
        Генерация информации о пользователе в виде словаря 
        """
        if not user:
            return {}
        return {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'password_hash': user.password_hash,
            'is_blocked': user.is_blocked,
            'created': user.created_at.strftime(format=settings.date_time_format)
        }

    async def create(self, name: str, email: str, password) -> dict:
        if await BaseService().get(self.model, email=email):
            return HTTPException(
                status_code=400,
                detail='User already exists'
            )
        await BaseService().create(
            self.model,
            email=email,
            name=name,
            password_hash=pbkdf2_sha512.hash(password),
        )
        return {
            'status': 'ok'
        }


    async def get(self, user: User, id: int):
        """
        Получение информации о пользователе для бэкенда
        """
        user_db = await BaseService().get(self.model, id=id)
        if not user:
            raise HTTPException(
                status_code=404,
                detail='User not found',
            )
        if user_db.id != user.id:
            raise HTTPException(
                status_code=401,
                detail='Cannot access to this user with your session',
            )
        return {
            'status': 'ok',
            'user': await UserService().generate_user_dict(user=user_db)
        }

    async def login(self, email: str, password: str):
        """
        Авторизация (проверка пароля + генерация токена)
        """
        user = await BaseService().get(self.model, email=email)
        if not user:
            raise HTTPException(
                status_code=404,
                detail='User was not found'
            )
        if not pbkdf2_sha512.verify(password, user.password_hash):
            raise HTTPException(
                status_code=401,
                detail='Wrong password'
            )
        return {
            'status': 'ok',
            'token': generate_token(email=email),
            'user_id': user.id,
            'name': user.name
        }
