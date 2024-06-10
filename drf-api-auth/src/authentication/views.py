from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings
import jwt
from datetime import datetime, timezone


# TODO: Manage refresh token


@api_view(['POST'])
def generate_token(request):
    
    user_id = request.data.get('user_id')
    if not user_id:
        return Response({'error': 'User ID not found'}, status=500)
    payload = {
        'user_id': user_id,
        'exp': datetime.now(timezone.utc) + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
        'iat': datetime.now(timezone.utc),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return Response({'access': token})


@api_view(['POST'])
def verify_token(request):
    token = request.data.get('token')
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return Response({'valid': True, 'payload': payload})
    except jwt.ExpiredSignatureError:
        return Response({'valid': False, 'error': 'Token expired'}, status=401)
    except jwt.InvalidTokenError:
        return Response({'valid': False, 'error': 'Invalid token'}, status=401)
    