from typing import List, Optional
from beanie import Document, Link

class Category(Document):
    name: str
    description: str
    depth: int = 0
    children: List[Optional[Link["Category"]]] = []
