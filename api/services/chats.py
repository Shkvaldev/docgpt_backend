from typing import List
from fastapi import HTTPException

from api.services.base import BaseService
from db.models import Chat
from config import settings

class ChatService:
    """
    Сервис для работы с чатами
    """
    def __init__(self):
        self.model = Chat

    @staticmethod
    async def generate_chat_dict(chat: Chat) -> dict:
        """
        Генерация информации о чате в виде словаря 
        """
        if not chat:
            return {}
        return {
            'id': chat.id,
            'user_id': chat.user_id,
            'created': chat.created_at.strftime(format=settings.date_time_format)
        }

    async def create(self, user_id: int) -> dict:
        """
        Создание нового чата
        """
        chat_db =  await BaseService().create(self.model, user_id=user_id)
        return {
            'status': 'ok',
            'chat': chat_db.id
        }
    
    async def get_chat(self, id: int, user_id: int) -> Chat:
        """
        Получение чата по id
        """
        chat_db = await BaseService().get(self.model, id=id)
        if not chat_db:
            raise HTTPException(
                status_code=404,
                detail='Chat was not found'
            )
        if chat_db.user_id != user_id:
            raise HTTPException(
                status_code=401,
                detail='Cannot access to this user with your session',
            )
        return {
            'status': 'ok',
            'chat': await ChatService.generate_chat_dict(chat_db)
        }
    

    async def get_chats(self, user_id: int) -> dict:
        """
        Получение всех чатов пользователя
        """
        chats_db = await BaseService().get_all(self.model, user_id=user_id)
        
        if not chats_db:
            return {
                'status': 'ok',
                'chats': []  
            }
        
        user_chats = [
            chat for chat in chats_db 
            if chat.user_id == user_id
        ]
        
        return {
            'status': 'ok',
            'chats': [await ChatService.generate_chat_dict(chat) for chat in user_chats]
        }

    async def delete(self, id: int, user_id: int) -> dict:
        """
        Удаление чата
        """
        chat_db = await BaseService().get(self.model, id=id)
        
        if not chat_db:
            raise HTTPException(
                status_code=404, 
                detail="Chat not found"
            )

        if chat_db.user_id != user_id:
            raise HTTPException(
                status_code=401,
                detail='Cannot access to this user with your session',
            )
        
        await BaseService().delete(self.model, id=id)
        return {
            "status": "ok"
        }

