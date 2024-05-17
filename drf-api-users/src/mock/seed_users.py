import requests
import json
from requests import Response

access_token = "b4ef6b00a1f605b16e9657628604397f184844acbbeb8dad84510415265da7e2"

response: Response = requests.get('https://api.intra.42.fr/v2/campus/25/users', headers={
    'Authorization': f'Bearer {access_token}'
})

# Parse the JSON response
json_response = response.json()

# Write the formatted JSON response to a file
with open('mock/mock_users.json', 'w') as file:
    json.dump(json_response, file, indent=4)