from typing import List, Optional, Union
from beanie import Document, Link

class Category(Document):
    name: str
    description: str
    depth: int = 0
    parents: List[Optional[Link["Category"]]] = [] 
    children: List[Optional[Link["Category"]]] = []
    docs: List[Optional[Link["Doc"]]] = []

class Doc(Document):
    name: str
    description: str
    file_id: str
    parents: List[Optional[Link["Category"]]] = []
