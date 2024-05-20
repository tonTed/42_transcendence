from ..constants import (
    GAME_CONSTS as GAME, 
    PADDLE_CONSTS as PADDLE, 
    CONTROLS_CONSTS as CTRL
)
from .paddle import Paddle

class Player:
    def __init__(self, id: int, paddle_x: int, goal: int) -> None:
        self.id = id
        self.paddle = Paddle(
            paddle_x, 
            PADDLE.INITIAL_Y, 
            PADDLE.HEIGHT, 
            PADDLE.WIDTH, 
            PADDLE.SPEED
        )
        self.score = 0
        self.controls = self.get_controls()
        self.goal = goal
        self.playing_side = (self.paddle.x > self.goal)
    
    def scored(self, ball_x: int) -> bool:
        if self.playing_side == GAME.LEFT_SIDE:
            return ball_x > self.goal
        else:
            return ball_x < self.goal

    def update_score(self) -> None:
        self.score += 1

    def get_controls(self) -> dict:
        if self.id == GAME.PLAYER1:
            return {'up': CTRL.P1_UP_KEY, 'down': CTRL.P1_DOWN_KEY}
        else:
            return {'up': CTRL.P2_UP_KEY, 'down': CTRL.P2_DOWN_KEY}