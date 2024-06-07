from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
import requests
import api.gateway
import api.ft
import os

BASE_URL = 'http://api-gateway:3000/api'


def topbar(request: HttpRequest) -> HttpResponse:

    id_42 = request.COOKIES.get('id42')

    user: dict = requests.get(f'{BASE_URL}/users/get_user_info_with_id_42/{id_42}')

    context: dict = {
        'user': user.json(),
    }
    return render(request, 'topbarNew.html', context=context)


def profile(request: HttpRequest) -> HttpResponse:

    id_42 = request.COOKIES.get('id42')

    user: dict = requests.get(f'{BASE_URL}/users/get_user_info_with_id_42/{id_42}')

    context: dict = {
        'user': user.json(),
    }
    return render(request, 'profileNew.html', context=context)


def friend_list(request: HttpRequest) -> HttpResponse:

    id_42 = request.COOKIES.get('id42')

    users: dict = requests.get(f'{BASE_URL}/users/').json()
    users_dict = list(filter(lambda user: user['id_42'] != str(id_42), users))
    context: dict = {
        'users': users_dict,
    }
    return render(request, 'sidebarNew.html', context=context)


def chat(request: HttpRequest) -> HttpResponse:

    mock_global_chat_messages: list[dict] = api.gateway.get_mock_global_chat_messages()
    context: dict = {
        'messages': mock_global_chat_messages,
    }
    return render(request, 'chatNew.html', context=context)


def pong(request: HttpRequest) -> HttpResponse:
    return render(request, 'pongNew.html')


CALLBACK_URL = (f'https://api.intra.42.fr/oauth/authorize'
                f'?client_id={os.getenv('42_UID')}'
                f'&redirect_uri=http://localhost/callback'
                f'&response_type=code'
                f'&scope=public')


def login(request: HttpRequest) -> HttpResponse:
    return render(request, 'loginNew.html', context={'url': CALLBACK_URL})


def callback(request) -> HttpResponse:

    access_token = api.ft.get_access_token_app(request.GET.get('code'))

    me = api.ft.get_me(access_token)

    user = requests.get(f'{BASE_URL}/users/get_user_info_with_id_42/{me["id_42"]}')

    if user.status_code == 404:
        user = requests.post(f'{BASE_URL}/users/create_user/', json=me)

    if user.json()['is_2fa_enabled']:
        return redirect('login_password', permanent=True)

    response: HttpResponse = redirect(f"/")
    response.set_cookie('token42', access_token)
    response.set_cookie('id42', me['id_42'])
    return response


def logout(request: HttpRequest) -> HttpResponse:
    response: HttpResponse = redirect(f"http://localhost")
    response.delete_cookie('token42')
    response.delete_cookie('id42')
    return response
