from django.views import View
import requests
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie

@csrf_protect
@ensure_csrf_cookie
def updateUsername(request, user_id):
    if request.method == 'PUT':
        url = f'http://api-users:3001/api/users/{user_id}/'
        response = requests.put(url, data=request.body, headers={'Content-Type': 'application/json'})
        return HttpResponse(response.content, status=response.status_code, content_type='application/json')
    return HttpResponse(status=405)


@api_view(['GET'])
def get_user_info(request, user_id):
    try:
        response = requests.get(f'http://api-users:3001/api/users/get_user_info/{user_id}')
        if response.status_code == 200:
            return JsonResponse(response.json(), status=200)
        else:
            return JsonResponse({'message': 'User not found'}, status=404)
    except requests.exceptions.RequestException as e:
        return JsonResponse({'message': 'Internal server error', 'error': str(e)}, status=500)