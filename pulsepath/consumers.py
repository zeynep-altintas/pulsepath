import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

class CrowdConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        #join channel group
        await self.channel_layer.group_add("room_crowd_updates", self.channel_name)

    async def disconnect(self, close_code):
        # Remove from group on disconnect
        await self.channel_layer.group_discard("room_crowd_updates", self.channel_name)

    async def crowd_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"]
        }))

