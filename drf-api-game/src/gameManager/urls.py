from django.urls import path
from .views import (
    GameListCreate,
    GameRetrieveUpdateDestroy,
    TournamentListCreate,
    TournamentRetrieveUpdateDestroy,
    get_user_game_data,
)

urlpatterns = [
    path("games/", GameListCreate.as_view(), name="game-list-create"),
    path("games/<int:pk>/", GameRetrieveUpdateDestroy.as_view(), name="game-detail"),
    path("tournaments/", TournamentListCreate.as_view(), name="tournament-list-create"),
    path(
        "tournaments/<int:pk>/",
        TournamentRetrieveUpdateDestroy.as_view(),
        name="tournament-detail",
    ),
    path("user_game_data/<int:user_id>/", get_user_game_data, name="user-game-data"),
]
