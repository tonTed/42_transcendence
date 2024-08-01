from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
import requests
from helpers.jwt_utils import extract_info_from_jwt, get_user_id_from_token
import os
import random
from pprint import pprint

# TODO: Manage errors and redirects for unauthorized access creatin a function that checks if the user is authorized
# TODO: Merge topbar and profil ?

BASE_URL = os.getenv('API_URL')


def add_status_to_users(users: list) -> list:
    statuses = ['online', 'offline', 'ingame']
    for user in users:
        user['status'] = random.choice(statuses)
    return users

@get_user_id_from_token
def topbar(request: HttpRequest) -> HttpResponse:

    user_id = request.user_id

    user: dict = requests.get(f'{BASE_URL}/users/{user_id}')

    context: dict = {
        'user': user.json(),
    }
    return render(request, 'topbar.html', context=context)


@get_user_id_from_token
def profile(request: HttpRequest) -> HttpResponse:

    user_id = request.user_id

    user: dict = requests.get(f'{BASE_URL}/users/{user_id}')

    context: dict = {
        'user': user.json(),
    }
    return render(request, 'profile.html', context=context)

@get_user_id_from_token
def form_game(request: HttpRequest) -> HttpResponse:

    user_id = request.user_id

    users: dict = requests.get(f'{BASE_URL}/users/').json()

    me = None
    users_list = []

    for user in users:
        if user['id'] == user_id:
            me = user
        else:
            users_list.append(user)

    pprint(users_list[0])

    context: dict = {
        'users': users_list,
        'me': me,
    }
    return render(request, 'form_game.html', context=context)


# TODO: Implement friend list create a schema for the friend list and refactor name to user-list
@get_user_id_from_token
def users_list(request: HttpRequest) -> HttpResponse:

    user_id = request.user_id

    users: dict = requests.get(f'{BASE_URL}/users/').json()

    me = None
    users_list = []

    for user in users:
        if user['id'] == user_id:
            me = user
        else:
            users_list.append(user)
    

    # REMOVE ME
    users_with_status = add_status_to_users(users_list)

    context: dict = {
        'users': users_with_status,
        'friends': me['friends'] if me else [],
    }
    return render(request, 'users_list.html', context=context)


def history(request: HttpRequest) -> HttpResponse:
    return render(request, 'history.html')
