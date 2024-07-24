import os
from django.shortcuts import render, redirect
import requests
import api.ft

API_URL = os.getenv('API_URL')

def handle_error(request, error_code, error_message):
    return render(request, 'error.html', {'error_code': error_code, 'error_message': error_message})

def get_access_token(code):
    try:
        access_token = api.ft.get_access_token(code)
        if not access_token:
            raise ValueError('Failed to get access token')
        return access_token
    except Exception as e:
        raise RuntimeError(f'Error getting access token: {str(e)}')

def get_me(access_token):
    try:
        me = api.ft.get_me(access_token)
        if not me:
            raise ValueError('Failed to get user information')
        return me
    except Exception as e:
        raise RuntimeError(f'Error getting user information: {str(e)}')

def get_user_info(me_id: str):
    try:
        user_response = requests.get(f'{API_URL}/users/get_user_info_with_id_42/{me_id}')
        if user_response.status_code == 404:
            return None, 404
        elif user_response.status_code != 200:
            raise ValueError("Failed to get user from API")
        return user_response.json(), 200
    except Exception as e:
        raise ValueError(f"Error getting user from API: {str(e)}")

def generate_jwt_token(user_id):
    try:
        jwt_response = requests.post(f'{API_URL}/auth/generate/', json={'user_id': user_id})
        if jwt_response.status_code != 200:
            raise ValueError('Failed to generate JWT token')
        jwt_token = jwt_response.json().get('access')
        if not jwt_token:
            raise ValueError('Invalid response when generating JWT token')
        return jwt_token
    except Exception as e:
        raise RuntimeError(f'Error generating JWT token: {str(e)}')

def generate_jwt_and_redirect(user_id):
    jwt_token = generate_jwt_token(user_id)
    response = redirect('/')
    response.set_cookie('jwt_token', jwt_token)
    return response, jwt_token