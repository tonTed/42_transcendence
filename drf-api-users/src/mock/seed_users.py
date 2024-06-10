import os
import sys
import json
import django
from users.models import User


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()


with open('mock/mock_users.json') as f:
    data = json.load(f)

for item in data:
    id_42 = item.get('id')
    username = item.get('login')
    email = item.get('email')
    avatar_url = item.get('image', {}).get('link')
    avatar = None

    if not User.objects.filter(id_42=id_42).exists():
        user = User.objects.create(
            id_42=id_42,
            username=username,
            email=email,
            avatar_url=avatar_url,
            avatar=avatar
        )
        user.save()
