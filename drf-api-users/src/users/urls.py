from django.urls import path
from users.views import UserListCreate, UserRetrieveUpdateDestroy, user_42


urlpatterns = [
    path('users/', UserListCreate.as_view(), name='user-view-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroy.as_view(), name='user-view-create'),
    path('users/42/<int:pk>/', user_42, name='user-42'),
]