from sqlalchemy import create_engine, delete, Select
from sqlalchemy.orm import sessionmaker
from config import settings

from db.base_model import Model


engine = create_engine(settings.get_uri())
Model.metadata.bind = engine
dbsession = sessionmaker(bind=engine, expire_on_commit=False)
session = dbsession()

# Базовый CRUD
def basic_create(db_model, **obj_data):
    db_obj = db_model(**obj_data)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def basic_get(db_model, **filters):
    result = session.execute(Select(db_model).filter_by(**filters))
    return result.scalars().first()


def basic_get_all(db_model, **filters):
    result = session.execute(Select(db_model).filter_by(**filters).order_by(db_model))
    return result.scalars().all()


def basic_get_all_asc(db_model, **filters):
    result = session.execute(Select(db_model).filter_by(**filters).order_by(db_model.id.asc()))
    return result.scalars().all()


def basic_get_all_desc(db_model, **filters):
    result = session.execute(Select(db_model).filter_by(**filters).order_by(db_model.id.desc()))
    return result.scalars().all()


def basic_update(db_obj: Model, **obj_in_data):
    for field, value in obj_in_data.items():
        setattr(db_obj, field, obj_in_data[field])
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def basic_delete(db_model, id_: int):
    session.execute(delete(db_model).where(db_model.id == id_))
    session.commit()
