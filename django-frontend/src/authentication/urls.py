from django.urls import path
from authentication.views import login, callback, logout, create_password, verify_2fa


urlpatterns = [
    path('frontend/login/', login, name='login'),
    path('callback/', callback, name='callback'),
    path('logout/', logout, name='logout'),
    path('frontend/create_password/', create_password, name='create_password'),
    path('frontend/verify_2fa/', verify_2fa, name='verify_2fa'),
]
