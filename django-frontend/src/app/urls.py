from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('frontend/', include('frontend.urls')),
    path('', include('authentication.urls')),
]
