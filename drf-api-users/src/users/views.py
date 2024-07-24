from rest_framework import generics
from rest_framework.decorators import api_view
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.auth.hashers import check_password


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


@api_view(['POST'])
def verify_password(request):
    try:
        user = User.objects.get(id=request.data['user_id'])
        if check_password(request.data['password'], user.password):
            return Response({'message': 'Password verified'}, status=200)
        else:
            return Response({'message': 'Password not verified'}, status=400)
    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=404)
