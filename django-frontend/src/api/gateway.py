import mock.friends
import api.ft

def get_friends() -> list[dict]:
    friends: list[dict] = mock.friends.get_friends()
    return friends

def get_user_info(access_token: str) -> dict:
    return api.ft.get_user_info(access_token=access_token)