from django.urls import path
from .views import get_user_info_with_id_42, updateUsername, updateAvatar, create_user, users, user_info

urlpatterns = (
    path('', users, name='create-user'),
    path('<int:id>/', user_info, name='user_info'),
    path('create_user/', create_user, name='create-user'),
    path('get_user_info_with_id_42/<int:id_42>/', get_user_info_with_id_42, name='get_user_info_with_id_42'),
    path('updateUsername/<int:user_id>/', updateUsername, name='user_update_username'),
    path('updateAvatar/<int:user_id>/', updateAvatar, name='user_update_avatar'),
)