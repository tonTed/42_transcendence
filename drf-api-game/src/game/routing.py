from django.urls import path
from .consumers import GameConnection

websocket_urlpatterns = [
    path('ws/game/', GameConnection.as_asgi()),
]
