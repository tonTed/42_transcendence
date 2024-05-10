from django.urls import path
from frontend.views import index, topbar, sidebar, chat, profile, game, gateway

urlpatterns = [
	path('', index, name='index'),
	path('topbar/', topbar, name='topbar'),
	path('sidebar/', sidebar, name='sidebar'),
	path('chat/', chat, name='chat'),

	# Profile
	path('profile/', profile, name='profile'),


	path('game/', game, name='game'),
	path('gateway/', gateway, name='gateway'),
]
