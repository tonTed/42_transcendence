from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests

AUTH_URL = 'http://api-auth:3003/auth'

@api_view(['POST'])
def generate_token(request):
    try:
        response = requests.post(
            'http://api-auth:3003/auth/generate/',
            json={'user_id': request.data.get('user_id')}
        )
        return Response(response.json())
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['POST'])
def verify_token(request):
    try:
        response = requests.post(
            'http://api-auth:3003/auth/verify/',
            json={'token': request.headers.get('Authorization')}
        )
        return Response(response.json(), status=response.status_code)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

