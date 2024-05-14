import mock.friends
import mock.chats
import api.ft

def get_friends() -> list[dict]:
    friends: list[dict] = mock.friends.get_friends()
    return friends

def get_friends_requests() -> list[dict]:
    friends_requests: list[dict] = mock.friends.get_friends_requests()
    return friends_requests

def get_friends_add() -> list[dict]:
    friends_add: list[dict] = mock.friends.get_friends_add()
    return friends_add

def get_user_info(access_token: str) -> dict:
    return api.ft.get_user_info(access_token=access_token)

def get_mock_global_chat_messages() -> list[dict]:
    mock_global_chat_messages: list[dict] = mock.chats.get_mock_global_chat_messages()
    return mock_global_chat_messages