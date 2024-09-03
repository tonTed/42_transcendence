from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'avatar_url',
            'email',
            'is_2fa_enabled',
            'id_42',
            'friends',
            'status',
            'password',
            'in_game'
        ]
