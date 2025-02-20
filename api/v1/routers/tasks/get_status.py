from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from loguru import logger

from mongodb.models import TaskStatus
from mongodb.services import MongoBaseService
from mongodb.database import mongo_init
from rabbitmq import update_tasks_status

router = APIRouter(
    prefix="/status"
)

@router.get('')
async def route(task_id: str):
    try:
        await mongo_init()
        await update_tasks_status()
        task_status = await MongoBaseService.find(TaskStatus, filters={"task_id": task_id})
        result = {'status': 'success', 'task': task_status.model_dump()}
        if task_status.status == "done":
            await MongoBaseService.delete(task_status)
        return result
    except Exception:
        return {'status': 'error', 'detail': 'Task was not found'} 

