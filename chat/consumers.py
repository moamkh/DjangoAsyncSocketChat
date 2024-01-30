import json

from asgiref.sync import  sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message



class ChatConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def get_room_obj(self):
        return Room.objects.filter(name__exact=self.room_name).prefetch_related('online').first()
    
    @database_sync_to_async
    def create_message_obj(self,message):
        return Message.objects.create(user=self.user, room=self.room, content=message)

    @database_sync_to_async
    def get_online_users(self):
        return self.room.online.all()
    
    @database_sync_to_async
    def set_online_user(self):
        return self.room.online.add(self.user)
    @database_sync_to_async
    def remove_online_user(self):
        return self.room.online.remove(self.user)


    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None
        self.user_inbox = None



    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.room = await self.get_room_obj()
        self.user = self.scope['user']
        self.user_inbox = f'inbox_{self.user.username}'

        # connection has to be accepted
        await self.accept()

        # join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        # send the user list to the newly joined user
        await self.send(json.dumps({
            'type': 'user_list',
            'users': [user.username for user in  await self.get_online_users()],
        }))

        if self.user.is_authenticated:
            # create a user inbox for private messages
            await self.channel_layer.group_add(
                self.user_inbox,
                self.channel_name,
            )

            # send the join event to the room
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_join',
                    'user': self.user.username,
                }
            )
            await self.set_online_user()
            # self.room.online.add(self.user)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

        if self.user.is_authenticated:
            # delete the user inbox for private messages
            await self.channel_layer.group_discard(
                self.user_inbox,
                self.channel_name,
            )

            # send the leave event to the room
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_leave',
                    'user': self.user.username,
                }
            )
            await self.remove_online_user()
            # self.room.online.remove(self.user)

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(f'{self.user}{message}')
        if not self.user.is_authenticated:
            return
        if message.startswith('/pm '):
            split = message.split(' ', 2)
            target = split[1]
            target_msg = split[2]

            # send private message to the target
            await self.channel_layer.group_send(
                f'inbox_{target}',
                {
                    'type': 'private_message',
                    'user': self.user.username,
                    'message': target_msg,
                }
            )
            # send private message delivered to the user
            await self.send(json.dumps({
                'type': 'private_message_delivered',
                'target': target,
                'message': target_msg,
            }))
            return

        # send chat message event to the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'user': self.user.username,
                'message': message,
            }
        )

        await self.create_message_obj(message)
        

    async def chat_message(self, event):
        print(event)
        await self.send(text_data=json.dumps(event))

    async def user_join(self, event):
        print(event)
        await self.send(text_data=json.dumps(event))

    async def user_leave(self, event):
        print(event)
        await self.send(text_data=json.dumps(event))

    async def private_message(self, event):
        print(event)
        await self.send(text_data=json.dumps(event))

    async def private_message_delivered(self, event):
        print(event)
        await self.send(text_data=json.dumps(event))
