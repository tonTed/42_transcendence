import os
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_protect
import requests
from liveUpdate.decorators import refresh_live_update
import jwt
import json
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
import time


USER_URL = os.getenv('USER_URL')


@api_view(['GET'])
def users(request):
    response = requests.get(f'{USER_URL}/')
    return HttpResponse(
        response.content,
        status=response.status_code,
        content_type=request.content_type
    )


@api_view(['GET'])
def user_info(request, user_id):
    response = requests.get(f'{USER_URL}/{user_id}')
    return HttpResponse(
        response.content,
        status=response.status_code,
    )


@csrf_protect
@api_view(['PATCH'])
@refresh_live_update(['topbar', 'users_list', 'profile'])
def update_username(request):
    jwt_token = request.COOKIES.get('jwt_token')
    payload = jwt.decode(jwt_token, options={"verify_signature": False}, algorithms=["none"])
    user_id = payload['user_id']
    response = requests.patch(
        f'{USER_URL}/{user_id}', data=request.body,
        headers={'Content-Type': request.content_type}
    )
    return HttpResponse(
        response.content,
        status=response.status_code,
    )


@api_view(['PATCH'])
@refresh_live_update(['users_list'])
def set_status(request):
    jwt_token = request.headers.get('Authorization')
    payload = jwt.decode(jwt_token, options={"verify_signature": False}, algorithms=["none"])
    user_id = payload['user_id']
    response = requests.patch(
        f'{USER_URL}/{user_id}', data=request.body,
        headers={'Content-Type': request.content_type}
    )
    return HttpResponse(
        response.content,
        status=response.status_code,
    )

@api_view(['PATCH'])
@refresh_live_update(['users_list'])
def set_ingame_status(request):
    jwt_token = request.headers.get('Authorization')
    payload = jwt.decode(jwt_token, options={"verify_signature": False}, algorithms=["none"])
    user_id = payload['user_id']
    response = requests.patch(
        f'{USER_URL}/{user_id}', data=request.body,
        headers={'Content-Type': request.content_type}
    )
    return HttpResponse(
        response.content,
        status=response.status_code,
    )

@csrf_protect
@api_view(['PATCH'])
@refresh_live_update(['profile', 'topbar'])
def update_avatar(request):
    jwt_token = request.COOKIES.get('jwt_token')
    payload = jwt.decode(jwt_token, options={"verify_signature": False}, algorithms=["none"])
    user_id = payload['user_id']
    
    if 'avatar' not in request.FILES:
        return HttpResponse(status=400)
    
    avatar_file: InMemoryUploadedFile = request.FILES['avatar']
    
    if avatar_file.size > settings.DATA_UPLOAD_MAX_MEMORY_SIZE:
        return HttpResponse(status=413)
    if avatar_file.content_type not in settings.ALLOWED_IMAGE_TYPES:
        return HttpResponse(status=415)
    
    image_extension = avatar_file.content_type.split("/")[1]
    file_name = f'avatar_{user_id}_{time.time()}.{image_extension}'
    file_path = f'{settings.MEDIA_ROOT}/{file_name}'
    with open(file_path, 'wb+') as destination:
        for chunk in avatar_file.chunks():
            destination.write(chunk)
    host = request.get_host()
    file_url = f'http://{host}/avatar/{file_name}'
    
    response = requests.patch(
        f'{USER_URL}/{user_id}', data=json.dumps({'avatar_url': file_url}),
        headers={'Content-Type': 'application/json'})
    return HttpResponse(
        response.content,
        status=response.status_code,
    )


@api_view(['PATCH'])
@refresh_live_update(['users_list'])
def update_friend_status(request):
    jwt_token = request.COOKIES.get('jwt_token')
    payload = jwt.decode(jwt_token, options={"verify_signature": False}, algorithms=["none"])
    user_id = payload['user_id']

    action = request.data['action']
    friend_id = request.data['friend_id']

    if action == 'add':
        response = requests.post(
            f'{USER_URL}/manage_friend/{user_id}/{friend_id}/',
            headers={'Content-Type': request.content_type})
        
    elif action == 'remove':
        response = requests.delete(
            f'{USER_URL}/manage_friend/{user_id}/{friend_id}/',
            headers={'Content-Type': request.content_type})
    
    return HttpResponse(
        response.content,
        status=response.status_code,
        content_type=request.content_type
    )

@refresh_live_update(['profile'])
def activate_2fa(request):
    jwt_token = request.COOKIES.get('jwt_token')
    payload = jwt.decode(jwt_token, options={"verify_signature": False}, algorithms=["none"])
    user_id = payload['user_id']
    response = requests.patch(
        f'{USER_URL}/{user_id}', data=json.dumps({'is_2fa_enabled': True}),
        headers={'Content-Type': request.content_type}
    )
    return HttpResponse(
        response.content,
        status=response.status_code,
        content_type=request.content_type
    )

@refresh_live_update(['profile'])
def deactivate_2fa(request):
    jwt_token = request.COOKIES.get('jwt_token')
    payload = jwt.decode(jwt_token, options={"verify_signature": False}, algorithms=["none"])
    user_id = payload['user_id']
    
    response = requests.patch(
        f'{USER_URL}/{user_id}', data=json.dumps({'is_2fa_enabled': False}),
        headers={'Content-Type': request.content_type}
    )
    return HttpResponse(
        response.content,
        status=response.status_code,
        content_type=request.content_type
    )

# TODO-GV: view to display history of game history from user_id (games wins, games lost, score, etc)