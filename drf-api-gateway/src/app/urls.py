from django.contrib import admin
from django.urls import path
from django.urls.conf import include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('user.urls')),
    path('api/auth/', include('authManager.urls')),
]
