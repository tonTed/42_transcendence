import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from game.game import Game
from game.constants import GAME_CONSTS


# TODO: Create an init method that initializes the game and starts the game loop
# TODO: Check JWT token and user_id to start the game
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
            if self.game.winner is None:
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
        actions = text_data_json.get('actions', {})

        if command == "actions":
            self.game.update_actions(actions)
