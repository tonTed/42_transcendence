from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
import requests
from drf_yasg.utils import swagger_auto_schema
from .swagger_schemas import game_creation_schema, tournament_creation_schema
from .serializer import (
    GameSerializer,
    GameUpdateSerializer,
    TournamentSerializer,
    TournamentUpdateSerializer
)

# Create your views here.
GAMES_URL = 'http://api-game:3002'


class GamesView(generics.ListCreateAPIView):
    serializer_class = GameSerializer
    
    def get(self, request):
        response = requests.get(f'{GAMES_URL}/games/')
        return Response(response.json())
    
    @game_creation_schema
    def post(self, request):
        response = requests.post(f'{GAMES_URL}/games/', json=request.data)
        return Response(response.json())
      
class GameView(generics.RetrieveUpdateAPIView):
    serializer_class = GameUpdateSerializer
    
    def get(self, request, game_id):
        response = requests.get(f'{GAMES_URL}/games/{game_id}/')
        return Response(response.json())
    
    def patch(self, request, game_id):
        response = requests.patch(f'{GAMES_URL}/games/{game_id}/', json=request.data)
        return Response(response.json())
    
    def put(self, request, game_id):
        return self.patch(request, game_id)
      
class TournamentsView(generics.ListCreateAPIView):
    serializer_class = TournamentSerializer
    
    def get(self, request):
        response = requests.get(f'{GAMES_URL}/tournaments/')
        return Response(response.json())
    
    @tournament_creation_schema
    def post(self, request):
        response = requests.post(f'{GAMES_URL}/tournaments/', json=request.data)
        return Response(response.json())
      
class TournamentView(generics.RetrieveUpdateAPIView):
    serializer_class = TournamentUpdateSerializer
    
    def get(self, request, tournament_id):
        response = requests.get(f'{GAMES_URL}/tournaments/{tournament_id}/')
        return Response(response.json())
    
    def patch(self, request, tournament_id):
        response = requests.patch(f'{GAMES_URL}/tournaments/{tournament_id}/', json=request.data)
        return Response(response.json())
    
    def put(self, request, tournament_id):
        return self.patch(request, tournament_id)