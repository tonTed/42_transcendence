from django.views import View
import requests
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_protect

@api_view(['POST'])
def create_user(request):
    response = requests.post('http://api-users:3001/users/', json=request.data)
    return HttpResponse(response.content, status=response.status_code, content_type=request.content_type)

@csrf_protect
@api_view(['PUT'])
def updateUsername(request, user_id):
    response = requests.put(f'http://api-users:3001/users/{user_id}', data=request.body, headers={'Content-Type': request.content_type})
    return HttpResponse(response.content, status=response.status_code, content_type=request.content_type)

@csrf_protect
@api_view(['PUT'])
def updateAvatar(request, user_id):
    response = requests.put(f'http://api-users:3001/users/{user_id}', data=request.body, headers={'Content-Type': request.content_type})
    return HttpResponse(response.content, status=response.status_code, content_type=request.content_type)


@api_view(['GET'])
def get_user_info_with_id42(request, user_id):
    response = requests.get(f'http://api-users:3001/users/get_user_info_with_id42/{user_id}')
    if response.status_code == 200:
        return JsonResponse(response.json(), status=200)
    else:
        return JsonResponse({'message': 'User not found'}, status=404)