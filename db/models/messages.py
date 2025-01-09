import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Relationship

from ..base_model import Model

class Message(Model):
    """
    Модель сообщения
    """
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String)
    role = Column(String)
    file_id = Column(Integer,  ForeignKey("files.id"), nullable=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    created_at = Column(DateTime, default=datetime.datetime.now)

    chat = Relationship('Chat', back_populates='messages', cascade='all')
    file = Relationship('File', back_populates='message', cascade='all, delete-orphan', uselist=False, single_parent=True,)