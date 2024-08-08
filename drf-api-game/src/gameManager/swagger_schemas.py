from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializer import GameSerializer

game_creation_schema = swagger_auto_schema(
    operation_description="Create a new game with a list of players (id and name)",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'players': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the player'),
                        'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the player'),
                    },
                    required=['id', 'name']
                ),
                description='List of players'
            ),
        },
        required=['players']
    ),
    responses={
        201: GameSerializer,
        400: 'Bad Request'
    }
)

tournament_creation_schema = game_creation_schema