import json

from channels.generic.websocket import WebsocketConsumer

class LiveUpdateConsumer(WebsocketConsumer):
    def connect(self):
        print("connected")
        self.accept()

    def disconnect(self):
        print("disconnected")
        pass
