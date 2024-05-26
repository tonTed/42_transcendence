from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from users.views import UserListCreate, UserRetrieveUpdateDestroy, get_user_info_with_id_42


urlpatterns = [
    path('users/', UserListCreate.as_view(), name='user-view-create'),
    path('users/<str:pk>', UserRetrieveUpdateDestroy.as_view(), name='user-view-create'),
    path('users/get_user_info_with_id_42/<int:id_42>/', get_user_info_with_id_42, name='user-info'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
