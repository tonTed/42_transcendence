from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError

def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return auth(request) # TEMPORARY AUTH using django built in auth

def sidebar(request):
    account_info = {
        'username': request.user.username,
        'email': request.user.email
    }
    return  render(request, 'sidebar.html', account_info)


# TEMPORARY AUTH using django built in auth for testing purpose
# THIS FUNCTION WILL MAKE CALLS TO THE DRF-API-GATEWAY AND/OR DRF-API-AUTH
def auth(request):
    # Handle registration
    if request.method == 'POST' and 'register' in request.POST:
        email = request.POST.get('emailInput')
        password = request.POST.get('passwordInput')
        username = request.POST.get('usernameInput')
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('index')
        except IntegrityError:
            messages.error(request, 'That email is already taken. Please choose another one.')
    # Handle login
    elif request.method == 'POST' and 'login' in request.POST:
        username = request.POST.get('usernameInput')
        password = request.POST.get('passwordInput')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid email or password')
    return render(request, 'auth.html')

# TEMPORARY LOGOUT for testing purpose
def logout_view(request):
    logout(request)
    return redirect('/')