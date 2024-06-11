from django.urls import path
from authentication.views import login, callback, logout


urlpatterns = [
    path('frontend/login/', login, name='login'),
    path('callback/', callback, name='callback'),
    path('logout/', logout, name='logout'),
]
