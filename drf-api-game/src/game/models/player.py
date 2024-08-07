from game.constants import (
    GAME_CONSTS as GAME, 
    PADDLE_CONSTS as PADDLE,
)
from game.models.paddle import Paddle


class Player:
    def __init__(self, player_id: int, paddle_x: int, goal: int) -> None:
        self.id = player_id
        self.paddle = Paddle(
            paddle_x, 
            PADDLE.INITIAL_Y, 
            PADDLE.HEIGHT, 
            PADDLE.WIDTH, 
            PADDLE.SPEED
        )
        self.score = 0
        self.goal = goal
        self.playing_side = (self.paddle.x > self.goal)
    
    def scored(self, ball_x: int) -> bool:
        if self.playing_side == GAME.LEFT_SIDE:
            return ball_x > self.goal
        else:
            return ball_x < self.goal

    def update_score(self) -> None:
        self.score += 1
