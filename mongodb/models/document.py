from typing import List, Optional
from beanie import Document, Link

from .category import Category

class Doc(Document):
    name: str
    description: str
    file_id: str
    parents: List[Optional[Link["Category"]]] = []
