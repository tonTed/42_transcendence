from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
import requests
import api.gateway
import api.ft
import os
import jwt

# TODO: Manage errors and redirects for unauthorized access creatin a function that checks if the user is authorized
# TODO: Merge topbar and profil ?

BASE_URL = os.getenv('API_URL')


def topbar(request: HttpRequest) -> HttpResponse:

    jwt_token = request.COOKIES.get('jwt_token')
    payload = jwt.decode(jwt_token, options={"verify_signature": False}, algorithms=["none"])
    user_id = payload['user_id']

    user: dict = requests.get(f'{BASE_URL}/users/{user_id}')

    context: dict = {
        'user': user.json(),
    }
    return render(request, 'topbar.html', context=context)


def profile(request: HttpRequest) -> HttpResponse:

    jwt_token = request.COOKIES.get('jwt_token')
    payload = jwt.decode(jwt_token, options={"verify_signature": False}, algorithms=["none"])
    user_id = payload['user_id']

    user: dict = requests.get(f'{BASE_URL}/users/{user_id}')

    context: dict = {
        'user': user.json(),
    }
    return render(request, 'profile.html', context=context)


# TODO: Implement friend list create a schema for the friend list and refactor name to user-list
def friend_list(request: HttpRequest) -> HttpResponse:

    jwt_token = request.COOKIES.get('jwt_token')
    payload = jwt.decode(jwt_token, options={"verify_signature": False}, algorithms=["none"])
    user_id = payload['user_id']

    users: dict = requests.get(f'{BASE_URL}/users/').json()
    users_dict = list(filter(lambda user: user['id'] != str(user_id), users))
    context: dict = {
        'users': users_dict,
    }
    return render(request, 'sidebar.html', context=context)


# TODO: Implement chat when all others todos are done
def chat(request: HttpRequest) -> HttpResponse:

    mock_global_chat_messages: list[dict] = api.gateway.get_mock_global_chat_messages()
    context: dict = {
        'messages': mock_global_chat_messages,
    }
    return render(request, 'chat.html', context=context)


# TODO: Useless views put template in static folder
def pong(request: HttpRequest) -> HttpResponse:
    return render(request, 'pong.html')
