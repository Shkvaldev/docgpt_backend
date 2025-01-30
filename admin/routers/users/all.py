from quart import Blueprint, render_template

from admin.utils import auth_required
from db.models import User
from admin.db.utils import basic_get_all_asc
from admin.db.users import generate_user_dict 

router = Blueprint(
    name='users_router_all',
    import_name='users_router_all'
)

# Show all users
@router.get('/all')
@auth_required
async def route():
    return await render_template('users/all.html', users=[
            generate_user_dict(user=user)
            for user in basic_get_all_asc(User)
        ]) 
