from db.models import User, Chat
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
        'created_at': chat.created_at.strftime(format=settings.date_time_format)
    }
