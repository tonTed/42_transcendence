from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
import requests
import api.gateway
import os


ID42 = '84489'

def topbar(request: HttpRequest) -> HttpResponse:

    id_42 = ID42

    user: dict = requests.get(f'http://api-gateway:3000/users/get_user_info_with_id_42/{id_42}').json()
    print(user)
    context: dict = {
        'user': user,
    }
    return render(request, 'topbarNew.html', context=context)


def friend_list(request: HttpRequest) -> HttpResponse:

    id_42 = ID42

    users: dict = requests.get(f'http://api-gateway:3000/users/').json()
    users_dict = list(filter(lambda user: user['id_42'] != str(id_42), users))
    context: dict = {
        'users': users_dict,
    }
    return render(request, 'sidebarNew.html', context=context)


def chat(request: HttpRequest) -> HttpResponse:

    id_42 = ID42

    mock_global_chat_messages: list[dict] = api.gateway.get_mock_global_chat_messages()
    context: dict = {
        'messages': mock_global_chat_messages,
    }
    return render(request, 'chatNew.html', context=context)


def pong(request: HttpRequest) -> HttpResponse:
    return render(request, 'pongNew.html')


CALLBACK_URL = (f'https://api.intra.42.fr/oauth/authorize'
                f'?client_id={os.getenv('42_UID')}'
                f'&redirect_uri=http://localhost:8000/app/callback/'
                f'&response_type=code'
                f'&scope=public')


def login(request: HttpRequest) -> HttpResponse:
    return render(request, 'loginNew.html', context={'url': CALLBACK_URL})


def callback(request) -> HttpResponse:

    response42 = requests.post('https://api.intra.42.fr/oauth/token', params={
        'grant_type': 'authorization_code',
        'client_id': os.getenv('42_UID'),
        'client_secret': os.getenv('42_SECRET'),
        'code': request.GET.get('code'),
        'redirect_uri': 'http://localhost:8000/app/callback/'
    })
    access_token = response42.json()['access_token']

    response: HttpResponse = redirect(f"http://localhost/app")
    response.set_cookie('token42', access_token)
    return response


