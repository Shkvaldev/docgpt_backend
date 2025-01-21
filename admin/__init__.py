from quart import Quart, request, redirect, url_for, render_template, session, g
from quart_cors import cors
from loguru import logger
from config import settings

from admin.utils import auth_required, auth
from admin.db.utils import generate_settings_dict
from admin.routers import routers

app = Quart(__name__)
app.secret_key = 'supersecret'

# Базовый CORS
# TODO: нормально настроить CORS
app = cors(app, allow_origin="*")

@app.get('/')
@auth_required
async def index(): 
    return await render_template('index.html', settings=generate_settings_dict(settings))

# Авторизация
@app.route('/login', methods=['GET', 'POST'])
async def login():
    if request.method == 'GET':
        return await render_template('login.html', not_authorized=True)
    # Логин в API
    logger.success("Logging in")
    form = await request.form
    email = form.get('email')
    password = form.get('password')
    try:
        data = auth(email=email, password=password)
    except Exception as e:
        return await render_template('error.html', not_authorized=True, error=str(e))
    session['token'] = data['token']
    session['user_info'] = data
    return redirect(url_for('index'))


# Отлавливаем
@app.errorhandler(404)
async def not_found(error):
    return await render_template('error.html', error='404 - Не найдено :(', not_authorized=True)


# Регистрация роутов
[app.register_blueprint(_route) for _route in routers]

@app.before_request
def save_context():
    g.app = app

def create_app():
    return app
