from django.urls import path
from .views import generate_token, verify_token


urlpatterns = [
    path('generate/', generate_token, name='generate_token'),
    path('verify/', verify_token, name='verify_token'),
]
