import jwt
from django.conf import settings
from django.http import JsonResponse


def extract_info_from_jwt(token, key):
    """
    Extract information from a JWT token.
    
    :param token: The JWT token.
    :param key: The key of the information to extract.
    :return: The extracted information or None if the key is not found.
    """
    try:
        payload = jwt.decode(token, options={"verify_signature": False}, algorithms=["none"])
        return payload.get(key)
    except jwt.ExpiredSignatureError:
        # Handle the case where the token has expired
        return None
    except jwt.InvalidTokenError:
        # Handle the case where the token is invalid
        return None


def get_user_id_from_token(view_func):
    def _wrapped_view(request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return JsonResponse({'error': 'Authorization header missing'}, status=401)
        user_id = extract_info_from_jwt(token, 'user_id')
        if not user_id:
            return JsonResponse({'error': 'Invalid or expired token'}, status=401)
        request.user_id = user_id
        return view_func(request, *args, **kwargs)

    return _wrapped_view
