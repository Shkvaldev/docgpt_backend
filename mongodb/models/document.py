from typing import List, Optional
from beanie import Document, Link

class Doc(Document):
    name: str
    description: str
    file_id: str
