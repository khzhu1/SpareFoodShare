from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from chatbox.models import Message
import json

User = get_user_model()

# to implement a online chat application using websockets
# this consumer class is inherited from AsyncWebsocketConsumer, 
# which is a class that implements the Asyncronise Websocket Protocol
class ChatConsumer(AsyncWebsocketConsumer):
    # this method is called when the websocket is opened
    async def connect(self):
        my_id = self.scope['user'].id
        other_user_id = self.scope['url_route']['kwargs']['id']
        if int(my_id) > int(other_user_id):
            self.room_name = f'{my_id}-{other_user_id}'
        else:
            self.room_name = f'{other_user_id}-{my_id}'

        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
    # this method is called when the websocket recieve a message
    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        sendto = data['id']
        if message:
            await self.save_message(username, sendto, self.room_group_name, message)
            # assign the message to the group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username,
                }
            )
    # this method is called when the group receives a message
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))

    # this method is called when the websocket is closed   
    async def disconnect(self, event):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def save_message(self, username, sendto, thread_name, message):
        '''
        This method is used to save the message to the database, 
        and also to create a thread for the message
        Input:
            username: username of the user who sent the message
            sendto: username of the user who received the message
            thread_name: name of the thread
            message: message sent by the user
        Output:
            None
        '''
        Message.objects.create(
            sender=username,
            sendto=sendto,
            thread_name=thread_name,
            message=message,
            
        )
