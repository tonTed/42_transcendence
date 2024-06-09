from django.urls import re_path

from liveUpdate.consumers import LiveUpdateConsumer

websocket_urlpatterns = [
    re_path(r"ws/live-update/$", LiveUpdateConsumer.as_asgi()),
]

