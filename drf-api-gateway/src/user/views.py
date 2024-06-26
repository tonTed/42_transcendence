import requests
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_protect
from liveUpdate.decorators import refresh_live_update
import jwt


# TODO: Add URL to user service in .env and const at beginning of file
# TODO: Create middleware to check if user is authorized and ignore some routes (like login)
# TODO: Remove id from path and use jwt token to get user id
# TODO: Manage if error occurs in requests
# TODO: Add verbose json data to response
# TODO: refactor to use jwt token to get user id

@api_view(['GET'])
def users(request):
    response = requests.get('http://api-users:3001/users/', json=request.data)
    return HttpResponse(response.content, status=response.status_code, content_type=request.content_type)


@api_view(['GET'])
def user_info(request, id):
    response = requests.get(f'http://api-users:3001/users/{id}')
    return HttpResponse(response.content, status=response.status_code, content_type=request.content_type)


@api_view(['POST'])
def create_user(request):
    response = requests.post('http://api-users:3001/users/', json=request.data)
    return HttpResponse(response.content, status=response.status_code, content_type=request.content_type)


@csrf_protect
@api_view(['PUT'])
@refresh_live_update(['topbar', 'friendList', 'profile'])
def updateUsername(request, user_id):
    jwt_token = request.COOKIES.get('jwt_token')
    payload = jwt.decode(jwt_token, options={"verify_signature": False}, algorithms=["none"])
    user_id = payload['user_id']
    response = requests.put(f'http://api-users:3001/users/{user_id}', data=request.body,
                            headers={'Content-Type': request.content_type})
    return HttpResponse(response.content, status=response.status_code, content_type=request.content_type)


@csrf_protect
@api_view(['PUT'])
def updateAvatar(request, user_id):
    jwt_token = request.COOKIES.get('jwt_token')
    payload = jwt.decode(jwt_token, options={"verify_signature": False}, algorithms=["none"])
    user_id = payload['user_id']
    response = requests.put(f'http://api-users:3001/users/{user_id}', data=request.body,
                            headers={'Content-Type': request.content_type})
    return HttpResponse(response.content, status=response.status_code, content_type=request.content_type)


@api_view(['GET'])
def get_user_info_with_id_42(request, id_42):
    response = requests.get(f'http://api-users:3001/users/get_user_info_with_id_42/{id_42}')
    if response.status_code == 200:
        return JsonResponse(response.json(), status=200)
    else:
        return JsonResponse({'message': 'User not found'}, status=404)
