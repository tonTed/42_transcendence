from django.urls import path
from .views import (
    update_username,
    update_avatar,
    create_user,
    users,
    user_info,
    set_status,
    update_friend_status,
    activate_2fa,
    deactivate_2fa
)


urlpatterns = (
    path('', users, name='create-user'),
    path('<int:user_id>/', user_info, name='user_info'),
    path('create_user/', create_user, name='create-user'),
    path('updateUsername/', update_username, name='user_update_username'),
    path('updateAvatar/', update_avatar, name='user_update_avatar'),
    path('set_status/', set_status, name='set_status'),
    path('update_friend_status/', update_friend_status, name='update_friend_status'),
    path('activate_2fa/', activate_2fa, name='activate_2fa'),
    path('deactivate_2fa/', deactivate_2fa, name='deactivate_2fa'),
)