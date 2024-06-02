import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Try to get the chat room, and handle the case where it does not exist
        try:
            self.chatroom = await database_sync_to_async(ChatRoom.objects.get)(name=self.room_name)
        except ChatRoom.DoesNotExist:
            # Close the connection if the chat room does not exist
            await self.close()
            return

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Load and send previous messages
        messages = await self.get_messages(self.chatroom)
        
        for message in messages:
            await self.send(text_data=json.dumps({
                'message': message['content'],
                'username': message['username'],
                'timestamp': message['timestamp']
            }))

    @database_sync_to_async
    def get_messages(self, chatroom):
        return [
            {
                'content': message.content,
                'username': message.sender.username,
                'timestamp': message.timestamp.strftime("%d-%m-%Y %H:%M")
            } 
            for message in Message.objects.filter(room=chatroom)
        ]

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        if message:
            chatroom = await database_sync_to_async(ChatRoom.objects.get)(name=self.room_name)
            message_obj = await database_sync_to_async(Message.objects.create)(
                sender=self.scope['user'],
                room=chatroom,
                content=message
            )
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': self.scope['user'].username,
                    'timestamp': message_obj.timestamp.strftime("%d-%m-%Y %H:%M")
                }
            )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        timestamp = event['timestamp']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'timestamp': timestamp
        }))
