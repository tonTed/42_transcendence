import os
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
import api.ft


CALLBACK_URL = (f'https://api.intra.42.fr/oauth/authorize'
                f'?client_id={os.getenv('42_UID')}'
                f'&redirect_uri={os.getenv('42_REDIRECT_URI')}'
                f'&response_type=code'
                f'&scope=public')


def login(request: HttpRequest) -> HttpResponse:
    return render(request, 'login.html', context={'url': CALLBACK_URL})


def logout(request: HttpRequest) -> HttpResponsePermanentRedirect:
    del request.session['token42']
    return redirect('index', permanent=True)


def callback(request) -> HttpResponsePermanentRedirect:
    access_token: str = api.ft.get_access_token(request.GET.get('code'))
    request.session['token42']: str = access_token
    return redirect('index', permanent=True)


def remove_session(request: HttpRequest) -> HttpResponsePermanentRedirect:
    request.session.flush()
    return redirect('index', permanent=True)
