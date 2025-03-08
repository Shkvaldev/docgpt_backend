from fastapi import WebSocket
from loguru import logger
from pydantic import BaseModel
from typing import Optional, Literal, List
from api.utils import get_current_user
from db.models import User
from api.services.messages import MessageService
from api.connection_manager_ws import ConnectionManager

from rabbitmq import push_task
from rabbitmq.task import Task
from mongodb.models import TaskStatus
from mongodb.services import MongoBaseService

class SendMessageSchema(BaseModel):
    action: Literal["send_message"]
    content: str
    role: str
    chat_id: int
    file_id: Optional[int] = None

class DeleteMessageSchema(BaseModel):
    action: Literal["delete_message"]
    id: int

class UpdateMessageSchema(BaseModel):
    action: Literal["update_message"]
    id: int
    content: str

class GetMessageSchema(BaseModel):
    action: Literal["get_message"]
    id: int

class GetChatMessagesSchema(BaseModel):
    action: Literal["get_chat_message"]
    chat_id: int

async def create_message(manager:ConnectionManager, data:dict, user:User, chat_id:int) -> None: 
    schema = SendMessageSchema(**data)
    
    message = await MessageService().create(
        chat_id=schema.chat_id,
        content=schema.content,
        role=schema.role,
        file_id=schema.file_id,
        user_id=user.id
        )
    message_data = {
        "action": "new_message",
        "chat_id": chat_id,
        "user_id": user.id,
        "content": message.content,
        "role": message.role,
        "file_id": message.file_id,
        "timestamp": str(message.timestamp)
    }
    
    # Creating task for rabbitmq
    # TODO!: add here parsing message or other stuff to define `type` header for worker
    if message_data["role"] != "bot":
        task = Task(
            status="pending",
            data=message_data
        )
        await push_task(task=task, headers={"type": "llm"})
    # Sending message to WS
    await manager.send_message(chat_id, message_data)

async def delete_message(manager:ConnectionManager, data:dict, user:User, chat_id:int) -> None:
    schema = DeleteMessageSchema(**data)
    await MessageService().delete(id=schema.id, user_id=user.id)
    await manager.send_message(chat_id, {"action": "message_deleted", "id": schema.id})

async def update_message(manager:ConnectionManager, data:dict, user:User, chat_id:int) -> None:
    schema = UpdateMessageSchema(**data)
    await MessageService().update(id=schema.id, user_id=user.id, content=schema.content)
    await manager.send_message(chat_id, {"action": "message_updated", "id": schema.id, "content": schema.content})

async def get_message( manager:ConnectionManager, data:dict, user:User, chat_id:int) -> None:
    schema = GetMessageSchema(**data)
    message = await MessageService().get_message(id=schema.id, user_id=user.id)
    if message:
        message_data = {
            "id": message.id,
            "chat_id": message.chat_id,
            "action": "message_data",
            "user_id": message.user_id,
            "content": message.content,
            "role": message.role,
            "file_id": message.file_id,
            "timestamp": str(message.timestamp)
        }
        await manager.send_message(chat_id, message_data)
    else:
        await manager.send_message(chat_id, {"error": "Message not found"})

async def get_chat_messages( manager:ConnectionManager, data:dict, user:User, chat_id:int) -> None:
    schema = GetChatMessagesSchema(**data)
    
    # Checking rabbitmq tasks
    task_statuses: Optional[List[TaskStatus]] = await MongoBaseService.find_all(TaskStatus, filters={"status": "done"}) 
    if task_statuses:
        for task_status in task_statuses:
            try:
                await MessageService().create(
                    chat_id=task_status.data["chat_id"],
                    content=task_status.data["content"],
                    role="bot",
                    user_id=task_status.data["user_id"],
                    file_id=task_status.data["file_id"] or None
                )
            except Exception as e:
                logger.error(f"Failed to create new message from bot: {e}")

    messages = await MessageService().get_messages(chat_id=schema.chat_id, user_id=user.id)
    messages_data = [
        {
            "id": msg.id,
            "chat_id": msg.chat_id,
            "user_id": msg.user_id,
            "content": msg.content,
            "role": msg.role,
            "file_id": msg.file_id,
            "timestamp": str(msg.timestamp)
        } for msg in messages
    ]
    await manager.send_message({"action": "chat_messages", "messages": messages_data})
