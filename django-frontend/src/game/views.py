from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def game(request: HttpRequest) -> HttpResponse :
    return (render(request, 'game/pong_game.html'))
