from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError

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
    return  render(request, 'sidebar.html', fake_account_info)

def game(request):
    return  render(request, 'game.html')

# THIS FUNCTION WILL MAKE CALLS TO THE DRF-API-GATEWAY AND/OR DRF-API-AUTH
def auth(request):
        return


# TEMPORARY LOGOUT for testing purpose
def logout_view(request):
    logout(request)
    return redirect('/')