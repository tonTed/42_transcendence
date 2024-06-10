from django.urls import path
from authentication.views import login, callback, logout, remove_session


# TODO: improve the URL patterns for login, woks with nginx configuration
urlpatterns = [
    path('frontend/login/', login, name='login'),
    path('callback/', callback, name='callback'),
    path('logout/', logout, name='logout'),
    path('remove_session/', remove_session, name='remove_session'),
]
