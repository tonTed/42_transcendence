import logging

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

logging.basicConfig(level=logging.DEBUG)


@api_view(['GET'])
def hello_world(request: Request):
    return Response({'message': 'Hello, World! From api Gateway'}, status=200)
