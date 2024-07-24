from django.urls import path
from authManager.views import generate_token, verify_token, verify_password


urlpatterns = [
    path('generate/', generate_token, name='generate_token'),
    path('verify/', verify_token, name='verify_token'),
    path('verify_password/', verify_password, name='verify_password'),
]
