from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
import requests
from helpers.jwt_utils import get_user_id_from_token
import os
import random
from pprint import pprint


API_URL = os.getenv('API_URL')


def add_status_to_users(users: list) -> list:
    statuses = ['online', 'offline', 'ingame']
    for user in users:
        user['status'] = random.choice(statuses)
    return users

@get_user_id_from_token
def topbar(request: HttpRequest) -> HttpResponse:
    
    authorization = request.headers.get('Authorization')
    user_id = request.user_id

    response: dict = requests.get(
        f'{API_URL}/users/{user_id}',
        headers={'Authorization': authorization}
    )
    if response.status_code != 200:
        return HttpResponse(status=response.status_code, content=response.reason)
    
    user: dict = response.json()
    
    context: dict = {
        'user': user,
    }
    return render(request, 'topbar.html', context=context)


@get_user_id_from_token
def profile(request: HttpRequest) -> HttpResponse:

    authorization = request.headers.get('Authorization')
    user_id = request.user_id

    response: dict = requests.get(
        f'{API_URL}/users/{user_id}',
        headers={'Authorization': authorization}
    )
    if response.status_code != 200:
        return HttpResponse(status=response.status_code, content=response.reason)
    
    user: dict = response.json()

    context: dict = {
        'user': user,
    }
    return render(request, 'profile.html', context=context)

@get_user_id_from_token
def form_game(request: HttpRequest) -> HttpResponse:

    authorization = request.headers.get('Authorization')
    user_id = request.user_id

    response: dict = requests.get(
        f'{API_URL}/users/',
        headers={'Authorization': authorization}
    )
    if response.status_code != 200:
        return HttpResponse(status=response.status_code, content=response.reason)
    
    users: dict = response.json()

    me = None
    users_list = []

    for user in users:
        if user['id'] == user_id:
            me = user
        else:
            users_list.append(user)

    context: dict = {
        'users': users_list,
        'me': me,
    }
    return render(request, 'form_game.html', context=context)


@get_user_id_from_token
def users_list(request: HttpRequest) -> HttpResponse:

    authorization = request.headers.get('Authorization')
    user_id = request.user_id

    response: dict = requests.get(
        f'{API_URL}/users/',
        headers={'Authorization': authorization}
    )
    if response.status_code != 200:
        return HttpResponse(status=response.status_code, content=response.reason)
    
    users: dict = response.json()
    response: dict = requests.get(
        f'{API_URL}/users/{user_id}',
        headers={'Authorization': authorization}
    )
    if response.status_code != 200:
        return HttpResponse(status=response.status_code, content=response.reason)
    
    me: dict = response.json()

    users_list = []
    friends_list = []

    for user in users:
        if user['id'] == user_id:
            continue
        elif me.get('friends') and user['id'] in me['friends']:
            friends_list.append(user)
        else:
            users_list.append(user)
    

    # TODO-TB: REMOVE ME
    users_with_status = add_status_to_users(users_list)
    friends_with_status = add_status_to_users(friends_list)

    context: dict = {
        'users': users_with_status,
        'friends': friends_with_status,
    }
    return render(request, 'users_list.html', context=context)


@get_user_id_from_token
def history(request: HttpRequest) -> HttpResponse:
    authorization = request.headers.get('Authorization')
    user_id = request.user_id

    response = requests.get(
        f'{API_URL}/games/',
        headers={'Authorization': authorization}
    )
    if response.status_code != 200:
        return HttpResponse(status=response.status_code, content=response.reason)
    
    all_games = response.json()
    current_user_games = [
        game for game in all_games
        if game['player1_id'] == user_id or game['player2_id'] == user_id
    ]
    games_played = len(current_user_games)
    wins = sum(1 for game in current_user_games if game['winner_id'] == user_id)
    losses = sum(1 for game in current_user_games if game['loser_id'] == user_id)
    goals_scored = sum(
        game['player1_score'] if game['player1_id'] == user_id else game['player2_score']
        for game in current_user_games
    )
    goals_conceded = sum(
        game['player2_score'] if game['player1_id'] == user_id else game['player1_score']
        for game in current_user_games
    )

    context = {
        'user_id': user_id,
        'all_games': all_games,
        'current_user_games': current_user_games,
        'games_played': games_played,
        'wins': wins,
        'losses': losses,
        'goals_scored': goals_scored,
        'goals_conceded': goals_conceded,
    }
    return render(request, 'history.html', context=context)
