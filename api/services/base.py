from sqlalchemy import Select, delete

from db.database import new_session

class BaseService:
    """
    Базовый CRUD+ менеджер, основной инструмент для работы других менеджеров
    """
    @staticmethod
    def get_session():
        return new_session()

    async def create(self, db_model, **obj_data):
        """
        Создание записи в базе данных
        """
        async with self.get_session() as session:
            db_obj = db_model(**obj_data)
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj

    async def get(self, db_model, **filters):
        """
        Получение записи из базы данных
        """
        async with self.get_session() as session:
            result = await session.execute(Select(db_model).order_by(db_model.id.desc()).filter_by(**filters))
            return result.scalars().first()

    async def get_all(self, db_model, **filters):
        """
        Получение всех записей из базы данных, которые удовлетворяют фильтрам
        """
        async with self.get_session() as session:
            result = await session.execute(Select(db_model).order_by(db_model.id.desc()).filter_by(**filters))
            return result.scalars().all()

    async def get_list(
            self,
            db_model,
            custom_where=None,
            custom_order=None,
            custom_limit=None,
            custom_offset=None,
            **filters,
    ) -> list:
        """
        Вспомогательный метод для получения записей списком из базы данных
        """
        custom_select = Select(db_model)
        if custom_where:
            custom_select = custom_select.where(custom_where)
        if custom_order:
            custom_select = custom_select.order_by(custom_order)
        if custom_limit:
            custom_select = custom_select.limit(custom_limit)
        if custom_offset:
            custom_select = custom_select.offset(custom_offset)
        async with self.get_session() as session:
            result = await session.execute(custom_select.filter_by(**filters))
            return result.scalars().all()

    async def search(self, db_model, custom_where=None, limit: int = 0, page: int = 1, **filters):
        """
        Поиск записей в базе данных по фильтрам. Возвращает список записей и их количество 
        """
        custom_limit, custom_offset = None, None
        if limit:
            custom_limit = limit
            custom_offset = custom_limit * (page - 1)
        result = await self.get_list(
            db_model,
            custom_where=custom_where,
            custom_limit=custom_limit,
            custom_offset=custom_offset,
            **filters
        )
        result_count = len(await self.get_list(db_model, custom_where=custom_where, **filters))
        return result, result_count

    async def update(self, db_obj, **obj_in_data):
        """
        Обновление данных в базе данных
        """
        async with self.get_session() as session:
            for field, value in obj_in_data.items():
                setattr(db_obj, field, obj_in_data[field])
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj

    async def delete(self, db_model, id: [str, int]):
        """
        Удаление записи из базы данных 
        """
        async with self.get_session() as session:
            await session.execute(delete(db_model).where(db_model.id == id))
            await session.commit()
    async def execute_query(self, query):
        """
        Выполнение произвольного запроса
        """
        async with self.get_session() as session:
            result = await session.execute(query)
            return result.scalar_one_or_none()
