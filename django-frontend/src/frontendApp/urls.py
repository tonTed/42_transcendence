from django.urls import path
from .views import topbar, friend_list, chat, pong, login, callback, profile


urlpatterns = [
    path('topbar/', topbar, name='profileNew'),
    path('friend_list/', friend_list, name='friend_listNew'),
    path('chat/', chat, name='chatNew'),
    path('pong/', pong, name='pongNew'),
    path('login/', login, name='loginNew'),
    path('callback/', callback, name='callbackNew'),
    path('profile/', profile, name='profileNew')
]