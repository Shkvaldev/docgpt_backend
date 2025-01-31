from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from pydantic import BaseModel
from typing import Optional, Literal
from api.utils import get_current_user
from db.models import User
from api.services.messages import MessageService
from connection_manager_ws import ConnectionManager

router = APIRouter(prefix="/ws")

manager = ConnectionManager()


from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from pydantic import ValidationError
from api.utils import get_current_user
from db.models import User
from api.services.messages import MessageService
from api.services.web_sockets import create_message, delete_message, update_message, get_message, get_chat_messages
#from .schemas import SendMessageSchema, DeleteMessageSchema, UpdateMessageSchema


@router.websocket("/chat/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: int, user: User = Depends(get_current_user)):
    await manager.connect(chat_id, user.id, websocket)
    try:
        while True:
            data = await websocket.receive_json()

            try:
                action = data.get("action")

                if action == "send_message":
                    await create_message(manager, data, user, chat_id)

                elif action == "delete_message":
                    await delete_message(manager, data, user, chat_id)

                elif action == "update_message":
                    await update_message(manager, data, user, chat_id)

                elif action == "get_message":
                    await get_message(websocket, manager, data, user, chat_id)

                elif action == "get_chat_message":
                    await get_chat_messages
                else:
                    await manager.send_message({"error": "Unknown action"})
            except ValidationError as e:
                await manager.send_message({"error": "Invalid data", "details": e.errors()})

    except WebSocketDisconnect:
        manager.disconnect(chat_id, user.id)

