from rest_framework import generics, status
from rest_framework.response import Response
from .models import Game, Tournament
from .serializer import GameSerializer, TournamentSerializer, GameUpdateSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import random
class GameListCreate(generics.ListCreateAPIView):

    queryset = Game.objects.all()
    serializer_class = GameSerializer

    @swagger_auto_schema(
        operation_description="Create a new game with a list of players (id and name)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'players': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the player'),
                            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the player'),
                        },
                        required=['id', 'name']
                    ),
                    description='List of players'
                ),
            },
            required=['players']
        ),
        responses={
            201: GameSerializer,
            400: 'Bad Request'
        }
    )
    def post(self, request, *args, **kwargs):
        players = request.data.get('players')

        if not players or len(players) != 2:
            return Response({"error": "A list of exactly two players is required."}, status=status.HTTP_400_BAD_REQUEST)

        player1 = players[0]
        player2 = players[1]

        player1_id = player1.get('id')
        player2_id = player2.get('id')
        player1_name = player1.get('name')
        player2_name = player2.get('name')

        if not player1_id or not player2_id or not player1_name or not player2_name:
            return Response({"error": "Each player must have an id and a name."}, status=status.HTTP_400_BAD_REQUEST)

        game = Game.objects.create(player1_id=player1_id, player2_id=player2_id)
        serializer = GameSerializer(game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class GameRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameUpdateSerializer

class TournamentListCreate(generics.ListCreateAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

class TournamentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer