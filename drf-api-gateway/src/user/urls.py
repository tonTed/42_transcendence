from django.urls import path
from .views import get_user_info, updateUsername

urlpatterns = [
	path('api/users/get_user_info/<int:user_id>/', get_user_info, name='get_user_info'),
    path('api/users/updateUsername/<int:user_id>/', updateUsername, name='user_update_username'),
]