import os
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
import api.ft
import requests
from requests import Response



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

    response: Response = requests.get('https://api.intra.42.fr/v2/me', headers={
        'Authorization': f'Bearer {access_token}'
    })

    user_id = response.json()["id"]
    request.session['id42'] = user_id

    # Check if user exists in the database
    user = requests.get(f'http://api-gateway:3000/api/users/get_user_info/{user_id}')
    if user.status_code == 404:
        requests.post('http://api-users:3001/api/users/', json={
            'id_42': user_id,
            'username': response.json()['login'],
            'avatar_url': response.json()['image']['versions']['small'],
            'email': response.json()['email'],
        })
        return redirect('index', permanent=True)

    if user.json()['is_2fa_enabled']:
        return redirect('login_password', permanent=True)
    return redirect('index', permanent=True)


def co(request: HttpRequest) -> HttpResponse:
    return render(request, 'index.html')


def remove_session(request: HttpRequest) -> HttpResponsePermanentRedirect:
    request.session.flush()
    return redirect('index', permanent=True)
