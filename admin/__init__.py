from flask import Flask, request, redirect, url_for, render_template, session
from flask_cors import CORS
from loguru import logger
from config import settings

from admin.utils import auth_required, auth
from admin.db.utils import generate_settings_dict
from admin.routers import routers

app = Flask(__name__)
app.secret_key = 'supersecret'

# Базовый CORS
# TODO: нормально настроить CORS
CORS(app)

@app.get('/')
@auth_required
def index(): 
    return render_template('index.html', settings=generate_settings_dict(settings))

# Авторизация
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', not_authorized=True)
    # Логин в API
    logger.success("Logging in")
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        data = auth(email=email, password=password)
    except Exception as e:
        return render_template('error.html', not_authorized=True, error=str(e))
    session['token'] = data['token']
    session['user_info'] = data
    return redirect(url_for('index'))


# Отлавливаем
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error='404 - Не найдено :(', not_authorized=True)


# Регистрация роутов
[app.register_blueprint(_route) for _route in routers]

def create_app():
    return app
