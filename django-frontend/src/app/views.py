from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .mock import fake_global_chat_messages
import api.ft
import api.gateway

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

def sidebar(request):
    friends: list[dict] = api.gateway.get_friends()
    friends_requests: list[dict] = api.gateway.get_friends_requests()
    friends_add: list[dict] = api.gateway.get_friends_add()

    context = {
        'friends': friends,
        'friends_add': friends_add,
        'friend_requests': friends_requests,
        'fake_global_chat_messages': fake_global_chat_messages,
    }
    return  render(request, 'sidebar.html', context)

def topbar(request):
    user: dict = api.gateway.get_user_info(request.session['token42'])
    context: dict = {
        'user': user,
    }
    return  render(request, 'topbar.html', context)

def profile(request):
    return  render(request, 'profile.html')