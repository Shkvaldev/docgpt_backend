from db.models import User, Chat, Message
from config import settings

def generate_user_dict(user: User):
    if not user:
        return {}
    return {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'is_admin': user.is_admin
    }

def generate_chat_dict(chat: Chat):
    if not chat:
        return {}
    return {
        'id': chat.id,
        'user_id': chat.user_id,
        'created_at': chat.created_at.strftime(format=settings.date_time_format)
    }

def generate_message_dict(message: Message):
    if not message:
        return {}
    result = {
        'id': message.id,
        'content': message.content,
        'role': message.role,
        'created_at': message.created_at.strftime(format=settings.date_time_format)
    }
    if message.file_id:
        result['file_id'] = message.file_id
    return result
