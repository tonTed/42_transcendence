from rest_framework import serializers
from users.models import User

# TODO: Remove password from serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'avatar',
            'avatar_url',
            'email',
            'is_2fa_enabled',
            'id_42',
            'friends',
            'password',
            'status'
        ]
