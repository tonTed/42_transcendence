from django.urls import path
from frontend.views import topbar, friend_list, pong, profile, history


urlpatterns = [
    path('topbar/', topbar, name='profile'),
    path('friend_list/', friend_list, name='friend_list'),
    path('history/', history, name='history'),
    path('pong/', pong, name='pong'),
    path('profile/', profile, name='profile'),
]
