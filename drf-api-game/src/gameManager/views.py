from rest_framework import generics, status
from rest_framework.response import Response
from .models import Game, Tournament
from .serializer import GameSerializer, TournamentSerializer, GameUpdateSerializer, TournamentUpdateSerializer
import random
from .swager_schema import game_creation_schema, tournament_creation_schema

class GameListCreate(generics.ListCreateAPIView):

    queryset = Game.objects.all()
    serializer_class = GameSerializer

    @game_creation_schema
    def post(self, request, *args, **kwargs):
        players = request.data.get('players')
        print(players)

        if not players or len(players) != 2:
            return Response({"error": "A list of exactly two players is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        player1 = players[0]
        player2 = players[1]

        player1_id = player1.get('id')
        player2_id = player2.get('id')
        player1_name = player1.get('name')
        player2_name = player2.get('name')

        # Check if any of the required fields are None
        if player1_id is None or player2_id is None or not player1_name or not player2_name:
            return Response({"error": "Each player must have an id and a name."}, status=status.HTTP_400_BAD_REQUEST)

        game = Game.objects.create(
            player1_id=player1_id, 
            player2_id=player2_id,
            player1_name=player1_name,
            player2_name=player2_name
        )
        serializer = GameSerializer(game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class GameRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameUpdateSerializer

class TournamentListCreate(generics.ListCreateAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    
    @tournament_creation_schema
    def post(self, request, *args, **kwargs):
        players = request.data.get('players')

        if not players or len(players) != 4:
            return Response({"error": "A list of exactly four players is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        random.shuffle(players)
       
        game1 = Game.objects.create(
            player1_id=players[0].get('id'), 
            player1_name=players[0].get('name'), 
            player2_id=players[1].get('id'), 
            player2_name=players[1].get('name')
        )
        game2 = Game.objects.create(
            player1_id=players[2].get('id'), 
            player1_name=players[2].get('name'), 
            player2_id=players[3].get('id'), 
            player2_name=players[3].get('name')
        )
        game3 = Game.objects.create()
        game4 = Game.objects.create()

        tournament = Tournament.objects.create()
        tournament.games.set([game1, game2, game3, game4])  
        return Response(TournamentSerializer(tournament).data, status=status.HTTP_201_CREATED)

class TournamentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentUpdateSerializer