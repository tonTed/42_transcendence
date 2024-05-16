import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from .game_logic import Game

class GameConnection(AsyncWebsocketConsumer):
    async def connect(self):
        self.game = Game()
        await self.accept()
        self.game_loop_task = asyncio.create_task(self.game_loop())

    async def disconnect(self, close_code):
        self.game_loop_task.cancel()

    async def game_loop(self):
        while True:
            await asyncio.sleep(1/70)
            self.game.update()
            await self.send_state()

    async def send_state(self):
        await self.send(text_data=json.dumps({
            'ball_position': {'x': self.game.ball.x, 'y': self.game.ball.y},
            'paddle1_position': {'y': self.game.paddle1.y},
            'paddle2_position': {'y': self.game.paddle2.y},
            'scores': {'player1': self.game.score1, 'player2': self.game.score2},
        }))
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        command = text_data_json['command']
        keys_pressed = text_data_json.get('keysPressed', {})

        if command == "keys":
            self.game.update_key_states(keys_pressed)
    

