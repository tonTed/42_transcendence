from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .mock import fake_account_info, fake_add_friends, fake_friends, fake_global_chat_messages, fake_friend_requests
import api.ft
import api.gateway

def index(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    if request.session.get('token42') is None:
        return redirect('login')

    user: dict = api.gateway.get_user_info(request.session['token42'])
    friends: list[dict] = api.gateway.get_friends()

    context: dict = {
        'user': user,
        'friends': friends,
        'other_users': 'other_users',
    }

    return render(request, 'index.html', context=context)

fake_account_info = {
    'username': 'fake_username',
    'email': 'fake_email'
}

def sidebar(request):
    context = {
        'fake_friends': fake_friends,
        'fake_add_friends': fake_add_friends,
        'fake_global_chat_messages': fake_global_chat_messages,
        'fake_friend_requests': fake_friend_requests,
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