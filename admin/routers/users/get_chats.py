from quart import Blueprint, render_template

from admin.utils import auth_required
from db.models import Chat
from admin.db.utils import basic_get_all_asc
from admin.db.users import generate_chat_dict 

router = Blueprint(
    name='users_router_get_chats',
    import_name='users_router_get_chats'
)

# Show all user's chats
@router.get('<user_id>/chats/get')
@auth_required
async def route(user_id):
    return await render_template('users/get_chats.html', chats=[
            generate_chat_dict(chat=chat)
            for chat in basic_get_all_asc(Chat, user_id=user_id)
        ]) 
