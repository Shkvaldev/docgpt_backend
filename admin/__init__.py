from flask import Flask
from loguru import logger
from config import settings

def create_app():
    app = Flask(__name__)
    return app
