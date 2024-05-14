from django.urls import path
from authentication.views import login, logout, remove_session, callback


urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('remove_session/', remove_session, name='remove_session'),
    path('callback/', callback, name='callback'),
]
