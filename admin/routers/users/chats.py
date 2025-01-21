from quart import Blueprint, render_template

from admin.utils import auth_required
from db.models import Chat
from admin.db.utils import basic_get_all_asc
from admin.db.users import generate_chat_dict 

router = Blueprint(
    name='users_router_chats',
    import_name='users_router_chats'
)

# Показ всех чатов пользователя
@router.get('/chats/get/<id>')
@auth_required
async def route(id):
    return await render_template('users/chats.html', chats=[
            generate_chat_dict(chat=chat)
            for chat in basic_get_all_asc(Chat, user_id=id)
        ]) 
