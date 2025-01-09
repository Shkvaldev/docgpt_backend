import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.orm import Relationship

from ..base_model import Model

class User(Model):
    """
    Модель пользователя
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String, unique=True)
    password_hash = Column(String)
    is_blocked = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    last_code = Column(String, nullable=True)
    code_expiration = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now)

    chats = Relationship('Chat', back_populates='user', cascade='all, delete-orphan')