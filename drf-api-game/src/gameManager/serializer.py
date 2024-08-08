from rest_framework import serializers
from .models import Game, Tournament

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

class GameUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['status', 'winner_id', 'player1_score', 'player2_score']

class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = '__all__'
        
class TournamentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ['status']