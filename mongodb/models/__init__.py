from typing import List, Optional, Union, Dict, Any
from beanie import Document, Link

class Category(Document):
    """
    Stores descriptions for documents categories (for graph)
    """
    name: str
    description: str
    depth: int = 0
    parents: List[Link["Category"]] = [] 
    children: List[Link["Category"]] = []
    docs: List[Link["Doc"]] = []

    class Settings:
        use_state_management = True

class Doc(Document):
    """
    Stores documents (for graph)
    """
    name: str
    description: str
    file_id: str
    categories: List[Link["Category"]] = []

    class Settings:
        use_state_management = True

class TaskStatus(Document):
    """
    Stores task's status
    """
    task_id: str
    status: str
    data: Dict[str, Any]

    class Settings:
        use_state_management = True
