from django.urls import path
from .views import updateUser

urlpatterns = [
    path('api/users/<int:user_id>/', updateUser.as_view(), name='user-update'),
]