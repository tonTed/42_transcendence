from django.http import HttpResponse
import requests
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie

@method_decorator(csrf_protect, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')
class updateUser(View):
    def put(self, request, user_id):
        url = f'http://api-users:3001/api/users/{user_id}/'
        response = requests.put(url, data=request.body, headers={'Content-Type': 'application/json'})
        return HttpResponse(response.content, status=response.status_code, content_type='application/json')
