import datetime
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import Relationship

from ..base_model import Model

class File(Model):
    """
    Модель файла
    """
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.now)

    message = Relationship('Message', back_populates='file', cascade='all, delete-orphan')
