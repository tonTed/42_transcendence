import os
import requests
from requests.models import Response


def get_access_token(code: str) -> str:
    response: Response = requests.post('https://api.intra.42.fr/oauth/token', params={
        'grant_type': 'authorization_code',
        'client_id': os.getenv('42_UID'),
        'client_secret': os.getenv('42_SECRET'),
        'code': code,
        'redirect_uri': os.getenv('42_REDIRECT_URI')
    })
    return response.json()['access_token']


def get_access_token_app(code: str) -> str:
    response: Response = requests.post('https://api.intra.42.fr/oauth/token', params={
        'grant_type': 'authorization_code',
        'client_id': os.getenv('42_UID'),
        'client_secret': os.getenv('42_SECRET'),
        'code': code,
        'redirect_uri': 'http://localhost:8000/app/callback/'
    })
    return response.json()['access_token']


def get_me(access_token: str):
    response: Response = requests.get('https://api.intra.42.fr/v2/me', headers={
        'Authorization': f'Bearer {access_token}'
    })

    return ({
        'id_42': response.json()['id'],
        'username': response.json()['login'],
        'avatar_url': response.json()['image']['versions']['small'],
        'email': response.json()['email'],
    })
