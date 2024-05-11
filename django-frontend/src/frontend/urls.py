from django.urls import path
from frontend.views import index, game, gateway

urlpatterns = [
	path('', index, name='index'),

	path('game/', game, name='game'),
	path('gateway/', gateway, name='gateway'),
]
