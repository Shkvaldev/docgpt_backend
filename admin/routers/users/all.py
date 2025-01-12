from flask import Blueprint

from admin.utils import auth_required

router = Blueprint(
    name='users_router_all',
    import_name='users_router_all'
)

# Показ всех пользователей
@router.get('/all')
@auth_required
def route():
    pass 
