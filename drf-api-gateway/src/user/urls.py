from django.urls import path
from .views import get_user_info, updateUsername, create_user

urlpatterns = [
	path('users/create_user/', create_user, name='create-user'),
	path('users/get_user_info/<int:user_id>/', get_user_info, name='get_user_info'),
    path('users/updateUsername/<int:user_id>/', updateUsername, name='user_update_username'),
]