from django.urls import path
from .views import updateUsername

urlpatterns = [
    path('api/users/updateUsername/<int:user_id>/', updateUsername.as_view(), name='user-update'),
]