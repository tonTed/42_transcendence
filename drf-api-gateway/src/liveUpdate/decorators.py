from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def refresh_live_update(routes_to_update):
    def decorator(func):
        def wrapper(*args, **kwargs):
            channel_layer = get_channel_layer()
            result = func(*args, **kwargs)
            if result.status_code == 200:
                async_to_sync(channel_layer.group_send)(
                    'live_update',
                    {'type': 'live_update', 'data': ','.join(routes_to_update)}
                )
            return result

        return wrapper

    return decorator
