from typing import List, Optional, Union
from beanie import Document, Link

from .document import Doc

class Category(Document):
    name: str
    description: str
    depth: int = 0
    parents: List[Optional[Link["Category"]]] = [] 
    children: List[Optional[Link["Category"]]] = []
    docs: List[Optional[Link["Doc"]]] = []
