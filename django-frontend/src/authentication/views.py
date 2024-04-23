import os

from django.shortcuts import render, redirect
from django.http import HttpRequest
import api.ft

CALLBACK_URL = (f'https://api.intra.42.fr/oauth/authorize'
                f'?client_id={os.getenv('42_UID')}'
                f'&redirect_uri={os.getenv('42_REDIRECT_URI')}'
                f'&response_type=code'
                f'&scope=public')


def login(request: HttpRequest):
    return render(request, 'login.html', context={'url': CALLBACK_URL})


def logout(request: HttpRequest):
    del request.session['token42']
    return redirect('index')


def callback(request):
    access_token = api.ft.get_access_token(request.GET.get('code'))
    request.session['token42'] = access_token
    return redirect('index')
