from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
import api.ft
import api.gateway
import requests


def index(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    if request.session.get('token42') is None:
        return redirect('login')
    
    user_id = request.session.get('id42')
    if user_id is None:
        return redirect('login')
    
    # FOR EXEMPLE ONLY WILL BE DELETED
    friends: list[dict] = api.gateway.get_friends()
    friends_requests: list[dict] = api.gateway.get_friends_requests()
    friends_add: list[dict] = api.gateway.get_friends_add()
    mock_global_chat_messages: list[dict] = api.gateway.get_mock_global_chat_messages()

    # context
    user_response = requests.get(f'http://api-gateway:3000/users/get_user_info/{user_id}')
    user: dict = user_response.json()

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


def login_password(request: HttpRequest) -> HttpResponse:
    if request.session.get('token42'):
        return redirect('index')
    return render(request, 'login_password.html')