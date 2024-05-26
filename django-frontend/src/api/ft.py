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