import requests
import json
import os
from requests import Response

access_token = "b4ef6b00a1f605b16e9657628604397f184844acbbeb8dad84510415265da7e2"


def get_users():
    if os.path.exists('mock_users.json'):
        return
    response: Response = requests.get('https://api.intra.42.fr/v2/campus/25/users', headers={
        'Authorization': f'Bearer {access_token}'
    })
    with open('mock_users.json', 'w') as file:
        json.dump(response.json(), file, indent=4)


if __name__ == '__main__':
    get_users()
