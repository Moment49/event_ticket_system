import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import RoomEvent, ChatMessages
import re
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = f"room_{self.scope['url_route']['kwargs']['room_name']}"
        self.room_name = re.sub(r" ", "_", self.room_name )
        print(self.scope)
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        self.close(close_code)
    
    async def receive(self, text_data=None):
        data_json = json.loads(text_data)
        print(text_data)

        event = {
            "type": "send_message",
            "message": data_json
        }

        await self.channel_layer.group_send(self.room_name, event)

    async def send_message(self, event):
        data = event["message"]
        await self.create_message(data = data)

        response = {
            "sender":data["sender"],
            "message":data["message"]
        }

        await self.send(text_data=json.dumps({"message":response}))

    @database_sync_to_async
    def create_message(self, data):
        get_room = RoomEvent.objects.get(room_event__name=data['room_event'])
        #check if user exists
        sender = CustomUser.objects.get(username=data['sender'])
        print(sender)
        if not ChatMessages.objects.filter(message=data['message'], 
                                           sender=sender).exists():
            
            new_message = ChatMessages.objects.create(room = get_room, message=data["message"], sender=sender)
            new_message.save()
