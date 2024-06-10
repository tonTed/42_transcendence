from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
import requests
from helpers.jwt_utils import extract_info_from_jwt, get_user_id_from_token
import os
import jwt

# TODO: Manage errors and redirects for unauthorized access creatin a function that checks if the user is authorized
# TODO: Merge topbar and profil ?

BASE_URL = os.getenv('API_URL')


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


# TODO: Implement friend list create a schema for the friend list and refactor name to user-list
@get_user_id_from_token
def friend_list(request: HttpRequest) -> HttpResponse:

    user_id = request.user_id

    users: dict = requests.get(f'{BASE_URL}/users/').json()
    users_dict = list(filter(lambda user: user['id'] != str(user_id), users))
    context: dict = {
        'users': users_dict,
    }
    return render(request, 'sidebar.html', context=context)


def history(request: HttpRequest) -> HttpResponse:
    return render(request, 'history.html')
