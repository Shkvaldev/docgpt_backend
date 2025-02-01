from typing import List, Optional
from beanie import PydanticObjectId
from loguru import logger

from mongodb.models import Category, Doc
from mongodb.services import MongoBaseService

class CategoryService:
    """
    Service for using `Category` model in mongodb
    """
    def __init__(self) -> None:
        self.model = Category


    async def create(
            self,
            name: str,
            description: str,
            depth: int,
            parents_ids: List[str] = [],
            children_ids: List[str] = [],
            docs_ids: List[str] = []
        ) -> Category:
        """
        Create new category
        """
        try:
            new_category = await MongoBaseService.create(
                model=Category,
                name=name,
                description=description,
                depth=depth
            )

            # Processing parents
            for parent_id in parents_ids:
                
                # Getting parent
                parent = await MongoBaseService.find(
                    model=Category,
                    filters={'_id': PydanticObjectId(parent_id)}
                )

                # Updating links for parent and new category
                parent.children.append(new_category)
                await MongoBaseService.update(parent)
                new_category.parents.append(parent)
            
            await MongoBaseService.update(new_category) 

            # Processing children
            for child_id in children_ids:
                
                # Getting children
                child = await MongoBaseService.find(
                    model=Category,
                    filters={'_id': PydanticObjectId(child_id)}
                )

                # Updating links for new category and it's child
                child.parents.append(new_category)
                await MongoBaseService.update(child)
                new_category.parents.append(child)
            
            await MongoBaseService.update(new_category)

            # Processing docs
            for doc_id in docs_ids:

                # Getting docs
                doc = await MongoBaseService.find(
                    model=Doc,
                    filters={'_id': PydanticObjectId(doc_id)}
                )

                # Updating links for new category
                doc.categories.append(new_category)
                await MongoBaseService.update(doc)
                new_category.docs.append(doc)
            
            await MongoBaseService.update(new_category)

            return new_category
        except Exception as e:
            raise ValueError(f"Failed to create category: {e}")
