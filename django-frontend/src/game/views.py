from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def gamedev(request: HttpRequest) -> HttpResponse :
    return (render(request, 'game/pong_game.html'))

