import mock.friends


def get_friends() -> list[dict]:
    friends: list[dict] = mock.friends.get_friends()
    return friends
