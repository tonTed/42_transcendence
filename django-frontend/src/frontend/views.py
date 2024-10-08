from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import requests
from helpers.jwt_utils import get_user_id_from_token
import os
import random


API_URL = os.getenv("API_URL")


def add_status_to_users(users: list) -> list:
    statuses = ["online", "offline", "ingame"]
    for user in users:
        user["status"] = random.choice(statuses)
    return users


@get_user_id_from_token
def topbar(request: HttpRequest) -> HttpResponse:

    authorization = request.headers.get("Authorization")
    user_id = request.user_id

    response: dict = requests.get(
        f"{API_URL}/users/{user_id}", headers={"Authorization": authorization}
    )
    if response.status_code != 200:
        return HttpResponse(status=response.status_code, content=response.reason)

    user: dict = response.json()

    context: dict = {
        "user": user,
    }
    return render(request, "topbar.html", context=context)


@get_user_id_from_token
def profile(request: HttpRequest) -> HttpResponse:

    authorization = request.headers.get("Authorization")
    user_id = request.user_id

    response: dict = requests.get(
        f"{API_URL}/users/{user_id}", headers={"Authorization": authorization}
    )
    if response.status_code != 200:
        return HttpResponse(status=response.status_code, content=response.reason)

    user: dict = response.json()

    context: dict = {
        "user": user,
    }
    return render(request, "profile.html", context=context)


@get_user_id_from_token
def form_game(request: HttpRequest) -> HttpResponse:

    authorization = request.headers.get("Authorization")
    user_id = request.user_id

    response: dict = requests.get(
        f"{API_URL}/users/", headers={"Authorization": authorization}
    )
    if response.status_code != 200:
        return HttpResponse(status=response.status_code, content=response.reason)

    users: dict = response.json()

    me = None
    users_list = []

    for user in users:
        if user["id"] == user_id:
            me = user
        else:
            users_list.append(user)

    context: dict = {
        "users": users_list,
        "me": me,
    }
    return render(request, "form_game.html", context=context)


@get_user_id_from_token
def users_list(request: HttpRequest) -> HttpResponse:

    authorization = request.headers.get("Authorization")
    user_id = request.user_id
    print(user_id)

    response: dict = requests.get(
        f"{API_URL}/users/", headers={"Authorization": authorization}
    )
    if response.status_code != 200:
        return HttpResponse(status=response.status_code, content=response.reason)

    users: dict = response.json()
    response: dict = requests.get(
        f"{API_URL}/users/{user_id}", headers={"Authorization": authorization}
    )
    if response.status_code != 200:
        return HttpResponse(status=response.status_code, content=response.reason)

    me: dict = response.json()

    users_list = []
    friends_list = []

    for user in users:
        if user["id"] == user_id:
            continue
        elif me.get("friends") and user["id"] in me["friends"]:
            friends_list.append(user)
        else:
            users_list.append(user)

    # TODO-TB: REMOVE ME
    # users_with_status = add_status_to_users(users_list)
    # friends_with_status = add_status_to_users(friends_list)

    context: dict = {
        "users": users_list,
        "friends": friends_list,
    }
    return render(request, "users_list.html", context=context)


@get_user_id_from_token
def history(request: HttpRequest) -> HttpResponse:
    authorization = request.headers.get("Authorization")
    user_id = request.GET.get("user_id")
    if user_id is None:
        user_id = request.user_id

    response: dict = requests.get(
        f"http://api-game:3002/user_game_data/{user_id}",
        headers={"Authorization": authorization},
    )
    user_game_data = response.json()

    response: dict = requests.get(
        f"{API_URL}/users/{user_id}", headers={"Authorization": authorization}
    )

    user_infos = response.json()

    context: dict = {
        "username": user_infos["username"],
        "game_history": user_game_data["games_history"],
        "user_stats": user_game_data["user_stats"],
    }

    return render(request, "history.html", context=context)
