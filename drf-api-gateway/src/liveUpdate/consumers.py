import json
import requests
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import urllib.parse
import jwt
import os

USER_URL = os.getenv("USER_URL")


class LiveUpdateConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.group_name = None

    def connect(self):
        self.group_name = "live_update"

        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        async_to_sync(self.get_params)()
        requests.patch(
            f"{USER_URL}/{self.user_id}",
            data=json.dumps({"status": "online"}),
            headers={"Content-Type": "application/json"},
        )
        async_to_sync(self.channel_layer.group_send)(
            "live_update", {"type": "live_update", "data": "users_list"}
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )
        requests.patch(
            f"{USER_URL}/{self.user_id}",
            data=json.dumps({"status": "offline"}),
            headers={"Content-Type": "application/json"},
        )
        async_to_sync(self.channel_layer.group_send)(
            "live_update", {"type": "live_update", "data": "users_list"}
        )
        print("disconnected")

    def live_update(self, event):
        print(f"live_update: {event}")
        self.send(text_data=json.dumps(event))

    def send(self, text_data=None, bytes_data=None, close=False):
        return super().send(text_data, bytes_data, close)

    async def get_params(self):
        query_string = self.scope["query_string"].decode()
        params = urllib.parse.parse_qs(query_string)
        jwt_token = params.get("jwt", [None])[0]
        payload = jwt.decode(
            jwt_token, options={"verify_signature": False}, algorithms=["none"]
        )
        self.user_id = payload["user_id"]
