import os
import requests
from django.http import HttpResponse
import re

AUTH_URL = os.getenv('AUTH_URL')


ignore_paths = [
  re.compile(r'^/api/auth/verify/$'),
  re.compile(r'^/api/users/get_user_info_with_id_42/.+$'),
  re.compile(r'^/api/users/create_user/$'),
  re.compile(r'^/api/auth/generate/$'),
  re.compile(r'^/api/auth/verify_password/$'),
]


#TODO-TB: use the token_access from 42 to verify the user for ignore_paths

class JWTAuthenticationMiddleware():
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    if any(pattern.match(request.path) for pattern in ignore_paths):
      return self.get_response(request)
    authorization = request.headers.get('Authorization')
    if not authorization:
      return HttpResponse(status=401, content='Unauthorized')
    response = requests.post(
      f'{AUTH_URL}/verify/',
      json={'token': authorization}
    )
    if response.status_code == 200:
      return self.get_response(request)
    return HttpResponse(status=401, content='Unauthorized')