from django.urls import path
from frontend.views import index, game, gateway, login_password

urlpatterns = [
	path('', index, name='index'),

	path('game/', game, name='game'),
	path('gateway/', gateway, name='gateway'),
	path('login/password/', login_password, name='login_password'),
]
