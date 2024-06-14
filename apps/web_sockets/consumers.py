import json
from channels.generic.websocket import AsyncWebsocketConsumer
from apps.web_sockets import constants as socket_constants

class SocketConsumer(AsyncWebsocketConsumer):
    """
    For sending messages from any view, use this code
    ```
        from asgiref.sync import async_to_sync
        from channels.layers import get_channel_layer

        from apps.web_sockets import constants as socket_constants

        layer = get_channel_layer()
        async_to_sync(layer.group_send)(socket_constants.default_group, {
            'type': 'send.message',
            'message': {'message': 'triggered'} # dict object to send as a message
        })
    ```
    """
    
    async def connect(self):
        try:
            await self.channel_layer.group_add(socket_constants.default_group, self.channel_name)
            await self.accept()
        except Exception as e:
            print(":::exception", e)
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            socket_constants.default_group,
            self.channel_name
        )
        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def send_message(self, event, type='message'):
        message = event['message']
        message['type'] = event.get('type', type)

        await self.send(text_data=json.dumps({'response': message}))

        