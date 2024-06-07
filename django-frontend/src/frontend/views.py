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
