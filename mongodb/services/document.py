import os
import uuid
import aiofiles
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
            file_content: bytes,
            file_name: Optional[str] = None
        ) -> Dict[str, str]:
        """
        Creates new document in mongodb.
        """
        # Saving file
        if file_name:
            file_path = f"{settings.upload_dir}/{file_name}"
        else:
            file_name = str(uuid.uuid4())+".docx"
            file_path = f"{settings.upload_dir}/{file_name}"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(file_content)
        
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
