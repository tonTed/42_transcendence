from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
import api.ft
import api.gateway
import requests


def index(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    if request.session.get('token42') is None:
        return redirect('login')

    user: dict = api.gateway.get_user_info(request.session['token42'])

    context: dict = {
        'user': user,
        'other_users': 'other_users',
    }
    return render(request, 'index.html', context=context)


def login(request):
    render(request, 'login.html')


def top_bar(request):
    user: dict = api.gateway.get_user_info(request.session['token42'])
    context: dict = {
        'user': user,
    }
    return render(request, 'topbar.html', context)


def sidebar(request):
    friends: list[dict] = api.gateway.get_friends()
    friends_requests: list[dict] = api.gateway.get_friends_requests()
    friends_add: list[dict] = api.gateway.get_friends_add()

    context = {
        'friends': friends,
        'friends_add': friends_add,
        'friend_requests': friends_requests,
    }
    return render(request, 'sidebar.html', context)


def chat(request):
    mock_global_chat_messages: list[dict] = api.gateway.get_mock_global_chat_messages()
    context = {
        'mock_global_chat_messages': mock_global_chat_messages,
    }
    return render(request, 'chat.html', context)


def profile(request):
    return render(request, 'profile.html')


def gateway(request: HttpRequest) -> HttpResponse:
    response = requests.get('http://api-gateway:3000/api/hello/')
    print(response.json())
    return HttpResponse(response.json())
