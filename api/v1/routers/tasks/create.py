from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from loguru import logger

from rabbitmq import push_task 
from rabbitmq.task import Task

router = APIRouter(
    prefix="/create"
)

class TaskGettingSchema(BaseModel):
    data: Dict[str, Any]

@router.post('')
async def route(schema: TaskGettingSchema):
    try:
        task = Task(status="pending", data=schema.data)
        task_id = await push_task(task)
        return {'status': 'success', 'task_id': task_id}
    except Exception as e:
        logger.error(f"Failed to create task: {e}")
        return HTTPException(status_code=500, detail='Failed to create task: connect support') 

