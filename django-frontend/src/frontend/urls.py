from django.urls import path
from frontend.views import topbar, friend_list, profile, history


urlpatterns = [
    path('topbar/', topbar, name='profile'),
    path('friend_list/', friend_list, name='friend_list'),
    path('history/', history, name='history'),
    path('profile/', profile, name='profile'),
]
