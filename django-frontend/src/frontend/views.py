from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
import api.ft
import api.gateway
import requests


def index(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    if request.session.get('token42') is None:
        return redirect('login')
    
    id42 = request.session.get('id42')
    if id42 is None:
        return redirect('login')

    user_response = api.gateway.get_user_info(id42)
    user: dict = user_response.json()

    friends: list[dict] = api.gateway.get_friends()
    friends_requests: list[dict] = api.gateway.get_friends_requests()
    friends_add: list[dict] = api.gateway.get_friends_add()
    mock_global_chat_messages: list[dict] = api.gateway.get_mock_global_chat_messages()

    context: dict = {
        'user': user,
        'other_users': 'other_users',
        'friends': friends,
        'friends_add': friends_add,
        'friend_requests': friends_requests,
        'mock_global_chat_messages': mock_global_chat_messages,
    }
    return render(request, 'index.html', context=context)


def login(request):
    render(request, 'login.html')


# Game
def game(request):
    return render(request, 'game.html')


def gateway(request: HttpRequest) -> HttpResponse:
    response = requests.get('http://api-gateway:3000/api/hello/')
    print(response.json())
    return HttpResponse(response.json())


def login_password(request: HttpRequest) -> HttpResponse:
    if request.session.get('token42'):
        return redirect('index')
    return render(request, 'login_password.html')