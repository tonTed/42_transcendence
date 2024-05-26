from django.urls import path
from .views import get_user_info_with_id_42, updateUsername, updateAvatar, create_user, users

urlpatterns = [
	path('users/', users, name='create-user'),
	path('users/create_user/', create_user, name='create-user'),
	path('users/get_user_info_with_id_42/<int:id_42>/', get_user_info_with_id_42, name='get_user_info_with_id_42'),
    path('users/updateUsername/<int:user_id>/', updateUsername, name='user_update_username'),
	path('users/updateAvatar/<int:user_id>/', updateAvatar, name='user_update_avatar'),
]