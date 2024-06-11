from django.urls import path
from authentication.views import login, callback, logout, create_password


urlpatterns = [
    path('frontend/login/', login, name='login'),
    path('callback/', callback, name='callback'),
    path('logout/', logout, name='logout'),
    path('frontend/create_password/', create_password, name='create_password'),
]
