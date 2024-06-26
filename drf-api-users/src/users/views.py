from rest_framework import generics
from rest_framework.decorators import api_view
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import status


class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)


@api_view(['GET'])
def get_user_info_with_id_42(request, id_42):
    try:
        user = User.objects.get(id_42=id_42)
        user_json = UserSerializer(user).data
        return Response(user_json, status=200)
    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=404)
