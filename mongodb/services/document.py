import os
import uuid
from typing import Dict, Optional

from mongodb.models import Doc
from mongodb.services import MongoBaseService
from config import settings

# NOTE: in fuct, this is an adapted replica of `api/services/files.py`

class DocService:
    """
    Service for using `Doc` model in mongodb
    """
    def __init__(self) -> None:
        self.model = Doc
    
    async def create(
            self,
            name: str,
            description: str,
            file_path: str
        ) -> Dict[str, str]:
        """
        Creates new document in mongodb.
        """
        
        # Saving to mongodb
        document = await MongoBaseService().create(
            self.model,
            name=name,
            description=description,
            file_id=file_path
        )
        
        return {
            'status': 'ok',
            'document_id': document.id
        }
