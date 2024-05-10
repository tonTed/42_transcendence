from django.urls import path
from frontend.views import index, topbar, sidebar, chat, profile, game, gateway, login_password

urlpatterns = [
	path('', index, name='index'),
	path('topbar/', topbar, name='topbar'),
	path('sidebar/', sidebar, name='sidebar'),
	path('chat/', chat, name='chat'),

	# Profile
	path('profile/', profile, name='profile'),


	path('game/', game, name='game'),
	path('gateway/', gateway, name='gateway'),
	path('login/password/', login_password, name='login_password'),
]
