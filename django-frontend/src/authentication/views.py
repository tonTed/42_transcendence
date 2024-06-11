import os
from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse, HttpResponsePermanentRedirect
import requests
import api.ft


API_URL = os.getenv('API_URL')

CALLBACK_URL = (f'https://api.intra.42.fr/oauth/authorize'
                f'?client_id={os.getenv("42_UID")}'
                f'&redirect_uri={os.getenv("42_REDIRECT_URI")}'
                f'&response_type=code'
                f'&scope=public')


def login(request: HttpRequest) -> HttpResponse:
    return render(request, 'login.html', context={'url': CALLBACK_URL})


# TODO: Manage errors:
# - request
# - access_token
# - me
# - user
# - jwt_token
# TODO: ask to password if new user
# TODO: ask to password if 2fa enabled
def callback(request) -> HttpResponse:

    access_token = api.ft.get_access_token(request.GET.get('code'))

    me = api.ft.get_me(access_token)

    user = requests.get(f'{API_URL}/users/get_user_info_with_id_42/{me["id_42"]}')

    if user.status_code == 404:
        # Rediriger vers une page pour créer un mot de passe
        request.session['me'] = me  # Stocker les données utilisateur dans la session
        return redirect('create_password')

    # if user.json()['is_2fa_enabled']:

    jwt_token = requests.post(f'{API_URL}/auth/generate/', json={'user_id': user.json()['id']})

    response: HttpResponse = redirect(f"/")
    response.set_cookie('jwt_token', jwt_token.json()['access'])
    return response


def logout(request: HttpRequest) -> HttpResponse:
    request.session.flush()
    response: HttpResponse = redirect(f"/")
    response.delete_cookie('jwt_token')
    return response


def create_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        me = request.session.get('me')
        me['password'] = password
        user_response = requests.post(f'{API_URL}/users/create_user/', json=me)
        
        if user_response.status_code == 201:
            user = user_response.json()
            jwt_token = requests.post(f'{API_URL}/auth/generate/', json={'user_id': user['id']})
            
            response = redirect('/')
            response.set_cookie('jwt_token', jwt_token.json()['access'])
            return response
        else:
            return render(request, 'create_password.html', {'error': 'Failed to create user'})
    
    return render(request, 'create_password.html')