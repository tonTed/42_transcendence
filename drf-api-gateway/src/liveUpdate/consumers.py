import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class LiveUpdateConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = 'live_update'

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )
        print("disconnected")

    def live_update(self, event):
        print(f"live_update: {event}")
        self.send(text_data=json.dumps(event))

    def send(self, text_data=None, bytes_data=None, close=False):
        return super().send(text_data, bytes_data, close)
