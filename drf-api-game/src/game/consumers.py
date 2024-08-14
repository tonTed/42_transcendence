import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from game.game import Game
from game.constants import GAME_CONSTS
from gameManager.views import update_game
from asgiref.sync import sync_to_async
import urllib.parse

class GameConnection(AsyncWebsocketConsumer):
    async def connect(self):
        # TODO-AR: check jwt (api/auth/verify) || voir index.js dans webserver (TEDDY)
      
        query_string = self.scope['query_string'].decode()
        params = urllib.parse.parse_qs(query_string)
        self.game_id = int(params.get('game_id', [None])[0])
        jwt = params.get('jwt', [None])[0]
        # TODO-AR: get host's id || voir drf-api-gateway/user/views.py line 51 (request)
        # TODO-AR: update status of host (request)
        # TODO-AR: fetch data game (with game id)
        # TODO-AR: update game status to "started" (request)
        self.game = Game()
        await self.accept()
        self.game_loop_task = asyncio.create_task(self.game_loop())
        
    async def update_game(self):
        game_data = {
            "status": "finished",
            "winner_id": self.game.winner,
            "player1_score": self.game.player1.score,
            "player2_score": self.game.player2.score
        }
        await sync_to_async(update_game)(self.game_id, game_data)

    async def game_ended(self):
        await self.update_game()
        await self.send_final()
        self.game_loop_task.cancel()
        # TODO-AR: update game status
        # TODO-AR: update host status
        await self.close()

    async def game_loop(self):
        while True:
            await asyncio.sleep(1 / GAME_CONSTS.FPS)
            if self.game.winner is None:
                self.game.update()
            else:
                await self.game_ended()
            await self.send_state()

    async def send_state(self):
        await self.send(text_data=json.dumps({
            'state': {
                'ball_position': {'x': self.game.ball.x, 'y': self.game.ball.y},
                'ball_radius': self.game.ball.radius,
                'paddle1_position': {'x': self.game.player1.paddle.x - self.game.player1.paddle.width / 2,
                                    'y': self.game.player1.paddle.y - self.game.player1.paddle.height / 2},
                'paddle2_position': {'x': self.game.player2.paddle.x - self.game.player2.paddle.width / 2,
                                    'y': self.game.player2.paddle.y - self.game.player2.paddle.height / 2},
                'paddle_height': self.game.player1.paddle.height,
                'paddle_width': self.game.player1.paddle.width,
                'scores': {'player1': self.game.player1.score, 'player2': self.game.player2.score},
                'resetting': self.game.resetting,
                'winner': self.game.winner
            }
        }))

    async def send_final(self):
        await self.send(text_data=json.dumps({
            'final': {
                'scores': {'player1': self.game.player1.score, 'player2': self.game.player2.score},
                'winner': self.game.winner
            }
        }))

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        command = text_data_json['command']
        actions = text_data_json.get('actions', {})

        if command == "actions":
            self.game.update_actions(actions)
