# chat/consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import socket


class ChatConsumer(AsyncWebsocketConsumer):
    user_name = ''
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # 여기서 조건달고 여러 함수들 실행하기

        
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.client", "message": message, "user_name": self.user_name}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
    



    async def chat_client(self, event):
        message = event["message"]
        userName = event["user_name"]

        await self.send(text_data=json.dumps({"message": userName + " : " + message}))