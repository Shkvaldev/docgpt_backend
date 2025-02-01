from typing import List, Optional, Union
from beanie import Document, Link

class Category(Document):
    name: str
    description: str
    depth: int = 0
    parents: List[Link["Category"]] = [] 
    children: List[Link["Category"]] = []
    docs: List[Link["Doc"]] = []

    class Settings:
        use_state_management = True

class Doc(Document):
    name: str
    description: str
    file_id: str
    categories: List[Link["Category"]] = []

    class Settings:
        use_state_management = True
