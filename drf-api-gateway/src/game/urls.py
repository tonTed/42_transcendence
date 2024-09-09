from django.urls import path
from .views import (
    GamesView,
    GameView,
    TournamentView,
    TournamentsView,
)


urlpatterns = (
    path('', GamesView.as_view(), name='games'),
    path('<int:game_id>/', GameView.as_view(), name='game'),
    path('tournaments/', TournamentsView.as_view(), name='tournaments'),
    path('tournaments/<int:tournament_id>/', TournamentView.as_view(), name='tournament'),
)