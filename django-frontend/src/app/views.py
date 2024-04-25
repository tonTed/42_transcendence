from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .mock import fake_account_info, fake_add_friends, fake_friends, fake_global_chat_messages, fake_friend_requests

fake_account_info = {
    'username': 'fake_username',
    'email': 'fake_email'
}

def index(request):
    # if user authenticated
        return render(request, 'index.html')
    # else:
    #     return auth(request)

def sidebar(request):
    context = {
        'fake_friends': fake_friends,
        'fake_add_friends': fake_add_friends,
        'fake_global_chat_messages': fake_global_chat_messages,
        'fake_friend_requests': fake_friend_requests,
    }
    return  render(request, 'sidebar.html', context)

def topbar(request):
    context = {
        'fake_account_info': fake_account_info,
    }
    return  render(request, 'topbar.html', context)

def profile(request):
    return  render(request, 'profile.html')

# THIS FUNCTION WILL MAKE CALLS TO THE DRF-API-GATEWAY AND/OR DRF-API-AUTH
def auth(request):
        return

# TEMPORARY LOGOUT for testing purpose
def logout_view(request):
    logout(request)
    return redirect('/')