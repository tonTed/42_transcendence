from django.urls import path
from .consumers import MyConsumer

websocket_urlpatterns = [
    path('ws/gamedev/', MyConsumer.as_asgi()),
]
