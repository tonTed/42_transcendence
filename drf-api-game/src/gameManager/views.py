from rest_framework import generics, status
from rest_framework.response import Response
from .models import Game, Tournament
from django.utils import timezone
from .serializer import (
    GameSerializer,
    TournamentSerializer
)
import random
from .swagger_schemas import game_creation_schema, tournament_creation_schema

class GameListCreate(generics.ListCreateAPIView):

    queryset = Game.objects.all()
    serializer_class = GameSerializer

    @game_creation_schema
    def post(self, request, *args, **kwargs):
        players = request.data.get('players')

        if not players or len(players) != 2:
            return Response({"error": "A list of exactly two players is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        player1 = players[0]
        player2 = players[1]

        player1_id = int(player1.get('id'))
        player2_id = int(player2.get('id'))
        player1_name = player1.get('name')
        player2_name = player2.get('name')

        # Check if any of the required fields are None
        if player1_id is None or player2_id is None or not player1_name or not player2_name:
            return Response({"error": "Each player must have an id and a name."}, status=status.HTTP_400_BAD_REQUEST)

        game = Game.objects.create(
            player1_id=player1_id, 
            player2_id=player2_id,
            player1_name=player1_name,
            player2_name=player2_name,
            date_time=timezone.now(),
        )
        serializer = GameSerializer(game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class GameRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class TournamentListCreate(generics.ListCreateAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    
    @tournament_creation_schema
    def post(self, request, *args, **kwargs):
        players = request.data.get('players')

        if not players or len(players) != 4:
            return Response({"error": "A list of exactly four players is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        random.shuffle(players)
       
        tournament = Tournament.objects.create()
        
        game1 = Game.objects.create(
            player1_id=players[0].get('id'), 
            player1_name=players[0].get('name'), 
            player2_id=players[1].get('id'), 
            player2_name=players[1].get('name'),
            tournament_id=tournament,
            date_time=timezone.now(),
        )
        game2 = Game.objects.create(
            player1_id=players[2].get('id'), 
            player1_name=players[2].get('name'), 
            player2_id=players[3].get('id'), 
            player2_name=players[3].get('name'),
            tournament_id=tournament,
            date_time=timezone.now(),
        )
        game3 = Game.objects.create(
            tournament_id=tournament,
            date_time=timezone.now(),
        )
        game4 = Game.objects.create(
            tournament_id=tournament,
            date_time=timezone.now(),
        )

        tournament.games.set([game1, game2, game3, game4])  
        return Response(TournamentSerializer(tournament).data, status=status.HTTP_201_CREATED)

class TournamentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    
#   "status": "not_started",
#   "winner_id": 2147483647,
#   "player1_score": 2147483647,
#   "player2_score": 2147483647
def update_game(game_id, game_data):
    try:
        game = Game.objects.get(id=game_id)
        tmp = game.status
        game.status = game_data.get('status')
        if game_data.get('winner_id') == 1:
            game.winner_id = game.player1_id
            game.loser_id = game.player2_id
        elif game_data.get('winner_id') == 2:
            game.winner_id = game.player2_id
            game.loser_id = game.player1_id
        game.player1_score = game_data.get('player1_score')
        game.player2_score = game_data.get('player2_score')
        if (tmp != game.status):
            game.date_time = timezone.now()
        game.save()
        if (game.tournament_id):
            update_tournament(game.tournament_id.id)
    except Exception as e:
        print(f"Error updating game: {e}")
        return False
    return True

def update_tournament(tournament_id):
    try:
        tournament = Tournament.objects.get(id=tournament_id)
        games = list(tournament.games.order_by('id'))
        game1, game2, game3, game4 = games[0], games[1], games[2], games[3]

        if (game1.status == 'in_progress'):
            tournament.status = 'in_progress'

        elif game1.status == 'finished' and game3.player1_id is None and game4.player1_id is None:
            game3.player1_id = game1.loser_id
            game3.player1_name = game1.player1_name if game1.loser_id == game1.player1_id else game1.player2_name
            game4.player1_id = game1.winner_id
            game4.player1_name = game1.player1_name if game1.winner_id == game1.player1_id else game1.player2_name
            game3.save()
            game4.save()

        elif game2.status == 'finished' and game3.player2_id is None and game4.player2_id is None:
            game3.player2_id = game2.loser_id
            game3.player2_name = game2.player1_name if game2.loser_id == game2.player1_id else game2.player2_name
            game4.player2_id = game2.winner_id
            game4.player2_name = game2.player1_name if game2.winner_id == game2.player1_id else game2.player2_name
            game3.save()
            game4.save()

        elif game4.status == 'finished':
            tournament.status = 'finished'
        
        elif any(game.status == 'cancelled' for game in [game1, game2, game3, game4]):
            tournament.status = 'cancelled'
            
        tournament.save()

    except Exception as e:
        print(f"Error updating tournament: {e}")
        return False
    return True
