import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Relationship

from ..base_model import Model

class Chat(Model):
    """
    Модель чата
    """
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.now)

    user = Relationship('User', back_populates='chats', cascade='all')
    messages = Relationship('Message', back_populates='chat', cascade='all, delete-orphan')
