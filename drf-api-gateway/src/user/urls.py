from django.urls import path
from .views import get_user_info_with_id42, updateUsername, updateAvatar, create_user

urlpatterns = [
	path('users/create_user/', create_user, name='create-user'),
	path('users/get_user_info_with_id42/<int:user_id>/', get_user_info_with_id42, name='get_user_info_with_id42'),
    path('users/updateUsername/<int:user_id>/', updateUsername, name='user_update_username'),
	path('users/updateAvatar/<int:user_id>/', updateAvatar, name='user_update_avatar'),
]