from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from loguru import logger

from mongodb.models import TaskStatus
from mongodb.services import MongoBaseService


router = APIRouter(
    prefix="/status"
)

@router.get('')
async def route(task_id: str):
    try:
        task_status = await MongoBaseService.find(TaskStatus, filters={"task_id": task_id})
        result = {'status': 'success', 'task': task_status.model_dump()}
        if task_status.status == "done":
            await MongoBaseService.delete(task_status)
        return result
    except Exception:
        return {'status': 'error', 'detail': 'Task was not found'} 

