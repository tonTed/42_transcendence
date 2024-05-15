from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'image_url', 'email', 'is_2fa_enabled', 'id_42', 'friends']