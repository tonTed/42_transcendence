from django.urls import path
from users.views import UserListCreate, UserRetrieveUpdateDestroy, get_user_id


urlpatterns = [
    path('users/', UserListCreate.as_view(), name='user-view-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroy.as_view(), name='user-view-create'),
    path('users/get_user_info/<int:user_id>/', get_user_id, name='user-42'),
]