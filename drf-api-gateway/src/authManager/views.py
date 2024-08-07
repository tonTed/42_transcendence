import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests

AUTH_URL = os.getenv('AUTH_URL')
USER_URL = os.getenv('USER_URL')

# TODO: Manage refresh token if needed and redirect to login page if token is expired
# TODO: Create middleware to check if user is authorized and ignore some routes (like login)


@api_view(['POST'])
def generate_token(request):
    try:
        response = requests.post(
            f'{AUTH_URL}/generate/',
            json={'user_id': request.data.get('user_id')}
        )
        return Response(response.json())
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['POST'])
def verify_token(request):
    try:
        response = requests.post(
            f'{AUTH_URL}/verify/',
            json={'token': request.headers.get('Authorization')}
        )
        return Response(response.json(), status=response.status_code)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['POST'])
def verify_password(request):
    print(request.data)
    response = requests.post(
        f'{USER_URL}/verify_password/',
        json=request.data
    )
    return Response(response.json(), status=response.status_code)
