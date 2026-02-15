import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')

        if message_type == 'chat_message':
            message = text_data_json['message']
            username = text_data_json['username']
            file_url = text_data_json.get('file_url', '')

            # Save message to database
            message_id = await self.save_message(username, self.room_name, message, file_url)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username,
                    'file_url': file_url,
                    'message_id': message_id # Send ID to clients
                }
            )
        elif message_type == 'delete_message':
            message_ids = text_data_json.get('message_ids', [])
            # Fallback for single message_id for backward compatibility (optional, but good practice)
            if not message_ids and 'message_id' in text_data_json:
                message_ids = [text_data_json['message_id']]

            username = text_data_json['username']
            
            # Delete from DB
            deleted_ids = await self.delete_message_db(message_ids, username)
            
            if deleted_ids:
                # Broadcast deletion to room
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message_delete',
                        'message_ids': deleted_ids
                    }
                )

        elif message_type == 'typing':
            username = text_data_json['username']
            is_typing = text_data_json['is_typing']

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_typing',
                    'username': username,
                    'is_typing': is_typing
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        file_url = event.get('file_url', '')
        message_id = event.get('message_id') # Get ID

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message,
            'username': username,
            'file_url': file_url,
            'message_id': message_id # Pass ID to client
        }))

    # Receive typing event from room group
    async def user_typing(self, event):
        username = event['username']
        is_typing = event['is_typing']

        await self.send(text_data=json.dumps({
            'type': 'typing',
            'username': username,
            'is_typing': is_typing
        }))

    # Receive deletion event from room group
    async def chat_message_delete(self, event):
        message_ids = event['message_ids']

        await self.send(text_data=json.dumps({
            'type': 'delete_message',
            'message_ids': message_ids
        }))

    @database_sync_to_async
    def save_message(self, username, room_name, message, file_url=None):
        from django.conf import settings
        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room_name)

        if file_url:
            # Robustly extract partial path from URL
            media_url = settings.MEDIA_URL
            if media_url in file_url:
                file_name = file_url.split(media_url)[-1]
                msg = Message.objects.create(user=user, room=room, content=message, file=file_name)
            else:
                 msg = Message.objects.create(user=user, room=room, content=message, file=file_url)
        else:
             msg = Message.objects.create(user=user, room=room, content=message)
        return msg.id

    @database_sync_to_async
    def delete_message_db(self, message_ids, username):
        deleted_ids = []
        try:
            # Filter messages by ID list AND user ownership
            messages = Message.objects.filter(id__in=message_ids, user__username=username)
            for msg in messages:
                deleted_ids.append(msg.id)
                msg.delete()
            return deleted_ids
        except Exception as e:
            print(f"Error deleting messages: {e}")
            return []
