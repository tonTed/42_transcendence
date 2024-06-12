from django.urls import path
from .views import get_user_info_with_id_42, update_username, update_avatar, create_user, users, user_info


urlpatterns = (
    path('', users, name='create-user'),
    path('<int:user_id>/', user_info, name='user_info'),
    path('create_user/', create_user, name='create-user'),
    path('get_user_info_with_id_42/<int:id_42>/', get_user_info_with_id_42, name='get_user_info_with_id_42'),
    path('updateUsername/', update_username, name='user_update_username'),
    path('updateAvatar/', update_avatar, name='user_update_avatar'),
)