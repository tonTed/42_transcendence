
mock_friends = [
    {
        'name': 'Teddy Blanco',
        'status': 'online'
    },
    {
        'name': 'Guillaume Vial',
        'status': 'offline'
    },
    {
        'name': 'Asaël Rivera',
        'status': 'in_game'
    }
]

mock_friends_requests = [
    { 'name': 'user5' },
    { 'name': 'user6' },
    { 'name': 'user5' },
]

mock_friends_add = [
    { 'name': 'user3' },
    { 'name': 'user4' },
    { 'name': 'user3' },
]

def get_friends() -> list:
    return mock_friends

def get_friends_requests() -> list:
    return mock_friends_requests

def get_friends_add() -> list:
    return mock_friends_add
