from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from app.views import generate_token, verify_token, verify_password


# TODO: create auth app to handle token generation, verification, and refresh
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('user.urls')),
    path('api/auth/generate/', generate_token, name='generate_token'),
    path('api/auth/verify/', verify_token, name='verify_token'),
    path('api/auth/verify_password/', verify_password, name='verify_password'),
]
