import json
import asyncio
from typing import Dict, Optional
from loguru import logger
import uuid
import aio_pika
from aio_pika import Message
from typing import Optional

from rabbitmq.task import Task
from mongodb.services import MongoBaseService
from mongodb.models import TaskStatus
from config import settings

async def create_queues():
    """
    Creates all needed rabbitmq queues
    """
    try:
        connection = await aio_pika.connect_robust(
            settings.get_rabbitmq_uri(),
        )
        async with connection:
            channel = await connection.channel()
            await channel.declare_queue("tasks")
            await channel.declare_queue("task_statuses")
            logger.success("All needed rabbitmq queues are declarated")
    except Exception as e:
        err_msg = f"Failed to create rabbitmq queues: {e}"
        logger.error(err_msg)
        raise ValueError(err_msg)

async def push_task(task: Task, headers: Dict[str, str] = {}):
    """
    Pushes task to rabbitmq
    """
    connection = await aio_pika.connect_robust(
        settings.get_rabbitmq_uri(),
    )
    async with connection:
        channel = await connection.channel()
        # Processing headers
        if "task_id" not in headers:
            headers["task_id"] = str(uuid.uuid4())

        await channel.declare_queue("tasks")
        
        # Create task
        await MongoBaseService.create(TaskStatus, task_id=headers["task_id"], status="pending", data=task.data)
         
        await channel.default_exchange.publish(
            Message(
                body=json.dumps(task.data).encode(),
                headers=headers
                ),
                routing_key="tasks",
        )
        logger.debug(f"New task `{headers['task_id']}` pushed to queue")
        return headers["task_id"]

async def update_tasks_status():
    """
    Gets task's info from rabbitmq
    """
    connection = await aio_pika.connect_robust(
        settings.get_rabbitmq_uri(),
    )

    # Buffer for gaining access to rabbitmq data
    # NOTE: please, don't change buffer dict to standalone var - dict is the only safe place
    buffer={"task_id": None, "task_data": None}

    # Rabbitmq message processing function
    async def process_message(message: Message):
        async with message.process():
            task_id = message.headers.get("task_id")
            if task_id is None:
                logger.warning("Received message without task_id. Ignoring message.")
                return
            
            buffer["task_id"] = task_id

            # Update status here
            try:
                buffer["task_data"] = json.loads(message.body.decode())
            except Exception as e:
                logger.error(f"Failed to decode task's message body from rabbitmq: task_id `{task_id}`, error: {e}")
                return

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("task_statuses")
        await queue.consume(process_message, no_ack=False)
    
    if not buffer["task_id"] or not buffer["task_data"]:
        return

    # Updating task in mongodb
    try:
        task_status_doc = await MongoBaseService.find(TaskStatus, filters={"task_id": buffer["task_id"]})
        # Update existing task status
        task_status_doc.status = buffer["task_data"]["status"]
        task_status_doc.data = buffer["task_data"]["data"] 
        await MongoBaseService.update(task_status_doc)
        logger.debug(f"Task's `{buffer["task_id"]}` status updated")
    except Exception as e:
        logger.error(f"Failed to update task with id `{buffer["task_id"]}`: {e}") 
        return
