from django.urls import path
from .views import login, logout, remove_session

urlpatterns = [
	path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('remove_session/', remove_session, name='remove_session'),
]
