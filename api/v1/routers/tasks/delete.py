from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from loguru import logger

from mongodb.models import TaskStatus
from mongodb.services import MongoBaseService

from rabbitmq import update_tasks_status

router = APIRouter(
    prefix="/delete"
)

@router.post('')
async def route(task_id: str):
    try:
        await update_tasks_status()
        task_status = await MongoBaseService.find(TaskStatus, filters={"task_id": task_id})
        await MongoBaseService.delete(task_status)
        logger.debug(f"Task `{task_id}` has been removed")
        return {'status': 'success'}
    except Exception as e:
        return {'status': 'error', 'detail': f'Failed to delete task `{task_id}`: {e}'}
