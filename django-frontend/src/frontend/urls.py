from django.urls import path
from frontend.views import topbar, users_list, profile, history, form_game


urlpatterns = [
    path('topbar/', topbar, name='profile'),
    path('users_list/', users_list, name='users_list'),
    path('history/', history, name='history'),
    path('profile/', profile, name='profile'),
    path('form_game/', form_game, name='form_game'),
]
