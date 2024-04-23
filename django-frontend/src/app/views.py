from django.shortcuts import render, redirect
from django.http import HttpRequest

import api.ft
import api.gateway


def index(request: HttpRequest):
    if request.session.get('token') is None:
        return redirect('login')
    user = api.ft.get_user_info(request.session['token'])

    friends = api.gateway.get_friends()

    context = {
        'user': user,
        'friends': friends,
        'other_users': 'other_users',
    }

    return render(request, 'index.html', context=context)

