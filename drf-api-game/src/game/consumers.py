import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from .game_logic import Game
from .constants import GAME_CONSTS

class GameConnection(AsyncWebsocketConsumer):
    async def connect(self):
        self.game = Game()
        await self.accept()
        self.game_loop_task = asyncio.create_task(self.game_loop())

    async def disconnect(self, close_code):
        self.game_loop_task.cancel()

    async def game_loop(self):
        while True:
            await asyncio.sleep(1 / GAME_CONSTS.FPS)
            if self.game.winner == None:
                self.game.update()
            await self.send_state()

    async def send_state(self):
        await self.send(text_data=json.dumps({
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
        }))

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        command = text_data_json['command']
        keys_pressed = text_data_json.get('keysPressed', {})

        if command == "keys":
            self.game.update_key_states(keys_pressed)
