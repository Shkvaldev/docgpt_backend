from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from api.services.base import BaseService
from db.models import Message, Chat
from config import settings
from api.services.chats import ChatService

class MessageService:
    """
    Сервис для работы с сообщениями
    """
    def __init__(self):
        self.model = Message

    @staticmethod
    async def generate_message_dict(message: Message) -> dict:
        """
        Генерация информации о сообщении в виде словаря 
        """
        if not message:
            return {}
        return {
            'id': message.id,
            'content': message.content,
            'role': message.role,
            'file_id': message.file_id,
            'chat_id': message.chat_id,
            'created': message.created_at.strftime(format=settings.date_time_format)
        }
    
    async def check_message_access(self, message_id: int, user_id: int) -> Message:
        """
        Проверка доступа пользователя к сообщению
        """
        # Создаем запрос с join
        query = (
            select(self.model)
            .options(joinedload(self.model.chat)) 
            .where(self.model.id == message_id)
        )
        
        # Получаем сообщение вместе с чатом
        message = await BaseService().execute_query(query)
        if not message:
            raise HTTPException(
                status_code=404,
                detail='Message was not found'
            )
            
        if message.chat.user_id != user_id:
            raise HTTPException(
                status_code=401,
                detail='Cannot access to this user with your session',
            )
            
        return message

    async def create(self, chat_id: int, content: str, role: str, user_id: int, file_id: int = None) -> dict:
        """
        Создание нового сообщения
        """
        # Получаем чат
        chat_db = await BaseService().get(Chat, id=chat_id)
        
        if not chat_db:
            raise HTTPException(
                status_code=404, 
                detail="Chat not found"
            )

        # Проверяем, принадлежит ли чат пользователю
        if chat_db.user_id != user_id:
            raise HTTPException(
                status_code=401,
                detail='Cannot access to this chat with your session',
            )
        
        # Создаем сообщение
        message_db = await BaseService().create(
            self.model,
            chat_id=chat_id,
            content=content,
            role=role,
            file_id=file_id
        )
        
        return {
            'status': 'ok',
            'message_id': message_db.id
        }

    async def get_message(self, id: int, user_id: int) -> dict:
        """
        Получение сообщения по id
        """
        message = await self.check_message_access(id, user_id)
        return {
            'status': 'ok',
            'message': await MessageService.generate_message_dict(message)
        }
    
    async def get_messages(self, chat_id: int, user_id: int) -> dict:
        """
        Получение всех сообщений чата
        """
        # Сначала проверяем доступ к чату
        await ChatService().get_chat(id=chat_id, user_id=user_id)
        
        # Получаем сообщения
        messages_db = await BaseService().get_all(self.model, chat_id=chat_id)
        
        # Если сообщений нет, возвращаем пустой список вместо 404
        if not messages_db:
            return {
                'status': 'ok',
                'messages': []
            }
            
        return {
            'status': 'ok',
            'messages': [
                await MessageService.generate_message_dict(message) 
                for message in messages_db
            ]
        }
    
    async def delete(self, id: int, user_id: int) -> dict:
        """
        Удаление сообщения
        """
        await self.check_message_access(id, user_id)
        await BaseService().delete(self.model, id=id)
        return {
            "status": "ok"
        }
    
    async def update(self, id: int, user_id: int, content: str) -> dict:
        """
        Обновление сообщения
        """
        message = await self.check_message_access(id, user_id)
        
        message.content = content
        updated_message = await BaseService().update(message)
        
        return {
            'status': 'ok',
            'message': await MessageService.generate_message_dict(updated_message)
        }