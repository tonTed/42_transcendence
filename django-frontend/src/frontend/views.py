from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
import api.ft
import api.gateway
import requests


def index(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    if request.session.get('token42') is None:
        return redirect('login')
    
    id_42 = request.session.get('id_42')
    if id_42 is None:
        return redirect('login')
    
    # FOR EXEMPLE ONLY WILL BE DELETED
    mock_global_chat_messages: list[dict] = api.gateway.get_mock_global_chat_messages()

    # context
    user: dict = requests.get(f'http://api-gateway:3000/users/get_user_info_with_id_42/{id_42}').json()
    users: dict = requests.get(f'http://api-gateway:3000/users/').json()
    users = list(filter(lambda user: user['id_42'] != str(id_42), users))

    context: dict = {
        'user': user,
        'users': users,
        'mock_global_chat_messages': mock_global_chat_messages,
    }
    return render(request, 'index.html', context=context)


def login_password(request: HttpRequest) -> HttpResponse:
    if request.session.get('token42'):
        return redirect('index')
    return render(request, 'login_password.html')