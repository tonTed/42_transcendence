from django.views import View
import requests
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie

@api_view(['POST'])
def create_user(request):
    response = requests.post('http://api-users:3001/users/', json=request.data)
    return HttpResponse(response.content, status=response.status_code, content_type='application/json')

@csrf_protect
@api_view(['PUT'])
def updateUsername(request, user_id):
    response = requests.put(f'http://api-users:3001/users/{user_id}/', data=request.body, headers={'Content-Type': 'application/json'})
    return HttpResponse(response.content, status=response.status_code, content_type='application/json')


@api_view(['GET'])
def get_user_info(request, user_id):
    response = requests.get(f'http://api-users:3001/users/get_user_info/{user_id}')
    if response.status_code == 200:
        return JsonResponse(response.json(), status=200)
    else:
        return JsonResponse({'message': 'User not found'}, status=404)