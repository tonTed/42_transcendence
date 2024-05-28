from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import requests
import api.gateway

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
