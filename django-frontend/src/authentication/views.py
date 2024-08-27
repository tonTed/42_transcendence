import os
from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse, HttpResponsePermanentRedirect
import requests
from authentication.helpers import get_access_token, get_me, get_user_info, generate_jwt_and_redirect, generate_jwt_token


API_URL = os.getenv('API_URL')
AUTH_URL = os.getenv('AUTH_URL')
USER_URL = os.getenv('USER_URL')

CALLBACK_URL = (f'https://api.intra.42.fr/oauth/authorize'
                f'?client_id={os.getenv("42_UID")}'
                f'&redirect_uri={os.getenv("42_REDIRECT_URI")}'
                f'&response_type=code'
                f'&scope=public')


def login(request: HttpRequest) -> HttpResponse:
    return render(request, 'login.html', context={'url': CALLBACK_URL})

def set_status(status: str, jwt_token: str) -> HttpResponse:
    cookies = {
        'jwt_token': jwt_token
    }
    response = requests.patch(f'{API_URL}/users/set_status/', json={'status': status}, cookies=cookies)
    return response

def callback(request: HttpRequest) -> HttpResponse:
    try:
        code = request.GET.get('code')
        if not code:
            return render(
                request,
                'error.html',
                {
                    'error_code': 400,
                    'error_message': 'Missing code parameter in request'
                }
            )

        access_token = get_access_token(code)
        me = get_me(access_token)
        user, status_code = get_user_info(me["id_42"])

        if status_code == 404:
            request.session['me'] = me
            return redirect('create_password')

        if user.get('is_2fa_enabled'):
            request.session['user_id'] = user['id']
            return redirect('verify_2fa')
        
        response, jwt_token = generate_jwt_and_redirect(user['id'])
        set_status('online', jwt_token)
        return response

    except ValueError as e:
        return render(request, 'error.html', {'error_code': 400, 'error_message': str(e)})
    except Exception as e:
        return render(request, 'error.html', {'error_code': 500, 'error_message': str(e)})


def logout(request: HttpRequest) -> HttpResponse:
    set_status('offline', request.COOKIES.get('jwt_token'))
    request.session.flush()
    response: HttpResponse = redirect(f"/")
    response.delete_cookie('jwt_token')
    return response


def create_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        me = request.session.get('me')
        me['password'] = password
        user_response = requests.post(f'{USER_URL}/users/', json=me)
        
        if user_response.status_code == 201:
            user = user_response.json()
            response, _ = generate_jwt_and_redirect(user['id'])
            return response
        else:
            return render(request, 'create_password.html', {'error': 'Failed to create user'})
    
    return render(request, 'create_password.html')


def verify_2fa(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        user_id = request.session.get('user_id')
        data = {
            'user_id': user_id,
            'password': password
        }
        auth_response = requests.post(f'{AUTH_URL}/auth/verify_password/', json=data)
        
        if auth_response.status_code == 200:
            response, _ = generate_jwt_and_redirect(user_id)
            return response
        else:
            return render(request, 'verify_2fa.html', {'error': 'Failed to verify 2FA'})
    
    return render(request, 'verify_2fa.html')