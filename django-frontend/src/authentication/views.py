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


def callback(request) -> HttpResponse:

    access_token = api.ft.get_access_token(request.GET.get('code'))

    me = api.ft.get_me(access_token)

    user = requests.get(f'{API_URL}/users/get_user_info_with_id_42/{me["id_42"]}')
    print(user.json())

    if user.status_code == 404:
        user = requests.post(f'{API_URL}/users/create_user/', json=me)

    if user.json()['is_2fa_enabled']:
        return redirect('login_password', permanent=True)

    response: HttpResponse = redirect(f"/")
    response.set_cookie('token42', access_token)
    response.set_cookie('id42', me['id_42'])
    response.set_cookie('id', user.json()['id'])
    return response


def logout(request: HttpRequest) -> HttpResponse:
    response: HttpResponse = redirect(f"http://localhost")
    response.delete_cookie('token42')
    response.delete_cookie('id42')
    response.delete_cookie('id')
    return response

def remove_session(request: HttpRequest) -> HttpResponsePermanentRedirect:
    request.session.flush()
    response: HttpResponse = redirect(f"/")
    response.delete_cookie('token42')
    response.delete_cookie('id42')
    response.delete_cookie('id')
    return response


