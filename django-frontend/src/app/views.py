from django.shortcuts import render, redirect
from django.http import HttpRequest

import api.ft


def index(request: HttpRequest):
    if request.session.get('token') is None:
        return redirect('login')
    user = api.ft.get_user_info(request.session['token'])
    return render(request, 'index.html', context={'user': user})

