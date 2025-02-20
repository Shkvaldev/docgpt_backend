from typing import Dict, Any
from pydantic import BaseModel

class Task(BaseModel):
    status: str
    data: Dict[str, Any]
