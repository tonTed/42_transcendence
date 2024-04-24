from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

import api.ft
import api.gateway
import requests


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


def gateway(request: HttpRequest) -> HttpResponse:
    response = requests.get('http://api-gateway:3000/api/hello/')
    print(response.json())
    return HttpResponse(response.json())
