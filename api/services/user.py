from datetime import datetime, timedelta
import string
import random
from loguru import logger
from passlib.hash import pbkdf2_sha512
from fastapi import HTTPException, BackgroundTasks
from pydantic import BaseModel, EmailStr

from api.services.base import BaseService
from db.models import User
from api.utils import generate_token, send_verification_code
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
            'is_blocked': user.is_blocked,
            'is_admin': user.is_admin,
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

    async def login(self, email: str, password: str, bg_tasks: BackgroundTasks):
        """
        Авторизация (проверка пароля)
        """
        user = await BaseService().get(self.model, email=email)
        if not user:
            raise HTTPException(
                status_code=404,
                detail='User was not found'
            )
        # Проверка на блок
        if user.is_blocked:
            raise HTTPException(
                status_code=401,
                detail='You are banned'
            )
        if not pbkdf2_sha512.verify(password, user.password_hash):
            raise HTTPException(
                status_code=401,
                detail='Wrong password'
            )
        # Если админ - сразу генерируем токен
        if user.is_admin:
            result = await UserService().generate_user_dict(user=user)
            result['token'] = generate_token(email=email)
            logger.debug(f"Admin with id `{user.id}` got login token")
            return result
        # Генерация одноразового кода
        code = "".join(random.choices(string.digits, k=6))
        # Отправка кода по email
        bg_tasks.add_task(send_verification_code, email, code)
        # Код истечёт через 15 минут
        expiration = datetime.now() + timedelta(minutes=15)
        await BaseService().update(user, last_code=code, code_expiration=expiration)
        return {
            'status': 'ok',
            'detail': 'Code is sent'
        }

    async def verify_code(self, email: str, code: str):
        """
        Верификация пользователя (проверка кода + генерация токена)
        """
        user = await BaseService().get(self.model, email=email)
        if not user:
            raise HTTPException(
                status_code=404,
                detail='User was not found'
            )
        # Проверка на наличие кода
        if not user.last_code:
            raise HTTPException(
                status_code=404,
                detail='You did not try to log in'
            )
        current_code = user.last_code
        expiration_time = user.code_expiration
        # Обнуление текущего кода
        await BaseService().update(user, last_code=None, code_expiration=None)
        # Проверка времени действия кода 
        if datetime.now() > expiration_time:
            raise HTTPException(
                status_code=401,
                detail='Code has been expired, request new please'
            )
        # Проверка соответствия кода
        if current_code != code:
            raise HTTPException(
                status_code=401,
                detail='Wrong code'
            )
        result = await UserService().generate_user_dict(user=user)
        result['token'] = generate_token(email=email)
        return result

    async def change_password(self, user: User, new_password: str):
        """
        Изменение пароля
        """
        try:
            await BaseService().update(user, password_hash=pbkdf2_sha512.hash(new_password))
        except Exception as e:
            logger.error(f'Failed to update password for `{user.email}`: {e}')
            raise HTTPException(
               status_code=500,
               detail='Failed to update password due to internal error'
            )
        return {
            'status': 'ok'
        }
