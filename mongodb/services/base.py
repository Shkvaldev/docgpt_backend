from typing import Dict, Any
from beanie import MergeStrategy

class MongoBaseService:
    """
    Basic mongodb service for dealing with document graph
    """
    @staticmethod
    async def create(model, **model_data):
        """
        Creates new data in mongodb
        """
        try:
            result = model(**model_data)
            await result.insert()
            return result
        except Exception as e:
            raise ValueError(f"Failed to create `{model}`: {e}")


    @staticmethod
    async def find(model, filters: Dict[str, Any]):
        """
        Finding one entity (`filters` is py dict in pymongo style)
        """
        try:
            result = await model.find_one(filters, fetch_links=True)
            if not result:
                raise ValueError("Not found")
            return result
        except Exception as e:
            raise ValueError(f"Failed to find one `{model}` with filters: {e}")


    @staticmethod
    async def find_all(model, filters: Dict[str, Any]):
        """
        Finding all entities (`filters` is py dict in pymongo style)
        """
        try:
            result = await model.find(filters, fetch_links=True).to_list()
            if not result:
                raise ValueError("Not found")
            return result
        except Exception as e:
            raise ValueError(f"Failed to find any `{model}` with filters: {e}")


    @staticmethod
    async def update(changed_model):
        """
        Updating changed model instance in mongodb
        """
        try:
            await changed_model.save()
        except Exception as e:
            raise ValueError(f"Failed to update model: {e}")


    @staticmethod
    async def delete(chosen_model):
        """
        Deleting model instance from mongodb
        """
        try:
            await chosen_model.delete()
        except Exception as e:
            raise ValueError(f"Failed to delete model: {e}")
