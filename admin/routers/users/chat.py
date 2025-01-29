from quart import Blueprint, render_template

from admin.utils import auth_required
from db.models import Message
from admin.db.utils import basic_get_all_asc
from admin.db.users import generate_message_dict 

router = Blueprint(
    name='users_router_chat',
    import_name='users_router_chat'
)

# Показ чата пользователя
@router.get('/<user_id>/chat/get/<chat_id>')
@auth_required
async def route(user_id, chat_id):
    return await render_template('users/chat.html', user_id=user_id, chat_id=chat_id, messages=[
            generate_message_dict(message=message)
            for message in basic_get_all_asc(Message, chat_id=chat_id)
        ])
