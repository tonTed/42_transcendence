import json
import asyncio
import requests
from channels.generic.websocket import AsyncWebsocketConsumer
from game.game import Game
from game.constants import GAME_CONSTS
from gameManager.views import update_game
from asgiref.sync import sync_to_async
import urllib.parse

class GameConnection(AsyncWebsocketConsumer):
    
    async def disconnect(self, code):
        if code != 1000:
            if self.game_loop_task:
                self.game_loop_task.cancel()
            await self.update_game('cancelled')
    
    async def connect(self):

        params = await self.get_params()

        self.game_loop_task = None
        self.game = Game()
        self.game_id = int(params.get('game_id', [None])[0])
        
        is_authorized = await self.is_authorized(params.get('jwt', [None])[0])
        
        if not is_authorized:
            await self.close(code=1401, reason="Unauthorized")
            return
        
        await self.update_host_status('in-game')
        await self.update_game('in_progress')
        await self.accept()
        self.game_loop_task = asyncio.create_task(self.game_loop())
        
    async def update_game(self, status='in_progress'):
        game_data = {
            "status": status,
            "winner_id": self.game.winner,
            "player1_score": self.game.player1.score,
            "player2_score": self.game.player2.score
        }
        await sync_to_async(update_game)(self.game_id, game_data)

    async def game_ended(self):
        await self.update_game('finished')
        await self.send_final()
        self.game_loop_task.cancel()
        await self.update_host_status('online')
        await self.close(code=1000, reason="Game ended")

    async def game_loop(self):
        while True:
            await asyncio.sleep(1 / GAME_CONSTS.FPS)
            if self.game.scored:
                self.game.scored = False
                await self.update_game()
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
            self.game.paused = False
            self.game.update_actions(actions)
        elif command == "pause":
            self.game.paused = True

    async def update_host_status(self, status: str):
        params = await self.get_params()
        jwt_token = params.get('jwt', [None])[0]
        cookies = {
            'jwt_token': jwt_token
        }
        response = requests.patch(
            'http://api-gateway:3000/api/users/set_status/', 
            json={'status': status},
            cookies=cookies)
        
    async def get_params(self):
        query_string = self.scope['query_string'].decode()
        params = urllib.parse.parse_qs(query_string)
        return params
    
    async def is_authorized(self, jwt_token):
        response = requests.post(
            'http://api-gateway:3000/api/auth/verify/',
            headers={'Authorization': jwt_token}
        )
        return response.status_code == 200
