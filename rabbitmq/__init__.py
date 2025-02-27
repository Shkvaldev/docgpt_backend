import json
import asyncio
from typing import Dict, Optional
from loguru import logger
import uuid
import aio_pika
from aio_pika import Message

from rabbitmq.task import Task
from mongodb.services import MongoBaseService
from mongodb.models import TaskStatus
from config import settings

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
    Gets task's info from rabbitmq (for fastapi lifespan)
    """
    logger.debug("Checking rabbitmq ... ")
    connection = await aio_pika.connect_robust(
        settings.get_rabbitmq_uri(),
    )

    async def process_message(message: Message):
        async with message.process():
            task_id = message.headers.get("task_id")
            if task_id is None:
                logger.warning("Received message without task_id. Ignoring message.")
                return
            
            try:
                task_data = json.loads(message.body.decode())
            except Exception as e:
                logger.error(f"Failed to decode task's message body from rabbitmq: task_id `{task_id}`, error: {e}")
                return
            # Update status here
            try:
                task_status_doc = await MongoBaseService.find(TaskStatus, filters={"task_id": task_id})
            except Exception:
                logger.error(f"Task with id `{task_id}` not found") 
                return
            # Update existing task status
            task_status_doc.status = task_data["status"]
            await MongoBaseService.update(task_status_doc)
            logger.debug(f"Task's `{task_id}` status updated")

    async with connection:
        channel = await connection.channel()
        # Declare queue for tasks
        await channel.declare_queue("tasks")
        queue = await channel.declare_queue("task_statuses")
        await queue.consume(process_message, no_ack=False)

"""
@app.on_event("startup")
async def startup_event():
    # Connect to RabbitMQ and start consuming messages
    connection = await aio_pika.connect_robust(settings.get_rabbitmq_uri())
    channel = await connection.channel()
    queue = await channel.declare_queue("task_statuses")

    async def process_message(message: Message):
        async with message.process():
            task_id = message.headers.get("task_id")
            if task_id is None:
                logger.warning("Received message without task_id. Ignoring message.")
                return

            status = message.body.decode()
            task_statuses[task_id] = status
            logger.debug(f"Task {task_id} status updated to {status}")

    await queue.consume(process_message, no_ack=False)
    yield
"""
