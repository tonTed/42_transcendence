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


# https://api.intra.42.fr/apidoc/2.0/users/me.html
def get_user_info(access_token: str) -> dict:
    response: Response = requests.get('https://api.intra.42.fr/v2/me', headers={
        'Authorization': f'Bearer {access_token}'
    })
    user = response.json()
    print(user)
    return {
        'login': user['login'],
        'email': user['email'],
        'first_name': user['first_name'],
        'last_name': user['last_name'],
        'full_name': user['displayname'],
        'image_url': user['image']['versions']['small'],
    }