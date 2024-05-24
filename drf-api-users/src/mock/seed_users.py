import os
import sys
import json
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

from users.models import User

with open('mock/mock_users.json') as f:
    data = json.load(f)

for item in data:
	username = item.get('login')
	email = item.get('email')
	avatar_url = item.get('image', {}).get('link')
	avatar = None

	user = User.objects.create(
		username=username,
		email=email,
		avatar_url=avatar_url,
		avatar=avatar
	)
	user.save()

print("Fake Users created")