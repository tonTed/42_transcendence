from rest_framework import generics, status
from rest_framework.response import Response
from .models import Game, Tournament
from .serializer import GameSerializer, TournamentSerializer, GameUpdateSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class GameListCreate(generics.ListCreateAPIView):

    queryset = Game.objects.all()
    serializer_class = GameSerializer

    @swagger_auto_schema(
        operation_description="Create a new game with player1_id and player2_id",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'player1_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of player 1'),
                'player2_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of player 2'),
            },
            required=['player1_id', 'player2_id']
        ),
        responses={
            201: GameSerializer,
            400: 'Bad Request'
        }
    )
    def post(self, request, *args, **kwargs):
        player1_id = request.data.get('player1_id')
        player2_id = request.data.get('player2_id')

        if not player1_id or not player2_id:
            return Response({"error": "player1_id and player2_id are required."}, status=status.HTTP_400_BAD_REQUEST)

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