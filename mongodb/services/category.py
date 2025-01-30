from typing import Optional
from loguru import logger

from mongodb.models import Category
from mongodb.services import MongoBaseService

class CategoryService:
    """
    Service for using `Category` model in mongodb
    """
    def __init__(self) -> None:
        self.model = Category


    async def as_child_of(self, parent: Category, **new_category_data):
        """
        Create new subcategory of chosen category
        """
        try:
            new_category = await MongoBaseService().create(self.model, **new_category_data)
            parent.children.append(new_category)
            new_category.depth = parent.depth + 1
            await MongoBaseService().update(new_category)
            return new_category
        except Exception as e:
            raise ValueError(f"Failed to create subcategory: {e}")
