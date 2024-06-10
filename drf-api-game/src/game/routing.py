from django.urls import path
from game.consumers import GameConnection


websocket_urlpatterns = [
    path('ws/game/', GameConnection.as_asgi()),
]
