import asyncio
from game.constants import (
    BALL_CONSTS as BALL,
    PADDLE_CONSTS as PADDLE,
    CANVAS_CONSTS as CANVAS,
    GAME_CONSTS as GAME,
)
from game.models.ball import Ball
from game.models.player import Player
from game.models.play_area import PlayArea
from game.collision_handler import CollisionHandler


class Game:
    def __init__(self) -> None:
        self.table = PlayArea(
            CANVAS.WIDTH / 2,
            CANVAS.HEIGHT / 2,
            CANVAS.WIDTH,
            CANVAS.HEIGHT
        )
        self.player1 = Player(
            GAME.PLAYER1,
            PADDLE.PADDLE1_X,
            self.table.right_goal
        )
        self.player2 = Player(
            GAME.PLAYER2,
            PADDLE.PADDLE2_X,
            self.table.left_goal
        )
        self.ball = Ball(
            BALL.INITIAL_X,
            BALL.INITIAL_Y,
            BALL.RADIUS,
            BALL.INITIAL_DX,
            BALL.INITIAL_DY,
            BALL.HIT_DX,
            BALL.COLLISION_COEFF
        )
        self.keys_pressed = {
            self.player1.controls['up']: False,
            self.player1.controls['down']: False,
            self.player2.controls['up']: False,
            self.player2.controls['down']: False,
        }
        self.resetting = True
        self.reset_time = GAME.INTERVAL_TIME
        self.reset_task = asyncio.create_task(self.reset_game())
        self.winner = None
        self.winning_score = GAME.WINNING_SCORE
        self.last_scorer = self.player2.id
        self.collision_handler = CollisionHandler(
            self.ball,
            self.player1.paddle,
            self.player2.paddle,
            self.table
        )

    def update_key_states(self, keys_pressed: dict) -> None:
        self.keys_pressed = keys_pressed

    def update(self) -> None:
        self.ball.update_position()
        self.player1.paddle.update_position(
            self.keys_pressed,
            self.player1.controls
        )
        self.player2.paddle.update_position(
            self.keys_pressed,
            self.player2.controls
        )
        self.check_collisions()
        if self.resetting is False and self.player_scored():
            self.reset_task = asyncio.create_task(self.reset_game())

    def check_collisions(self) -> None:
        self.collision_handler.ball_and_paddles()
        self.collision_handler.ball_and_boundaries()
        self.collision_handler.paddles_and_boundaries()

    def player_won(self, score: int) -> bool:
        return score >= self.winning_score

    def player_scored(self) -> bool:
        if self.player1.scored(self.ball.x):
            self.player1.update_score()
            self.last_scorer = self.player1.id
            if self.player_won(self.player1.score):
                self.winner = self.player1.id
            return True
        elif self.player2.scored(self.ball.x):
            self.player2.update_score()
            self.last_scorer = self.player2.id
            if self.player_won(self.player2.score):
                self.winner = self.player2.id
            return True
        return False

    async def reset_game(self) -> None:
        self.resetting = True
        await asyncio.sleep(self.reset_time)
        self.serve()
        self.resetting = False

    def serve(self) -> None:
        if self.last_scorer == self.player1.id:
            dx, dy = self.get_serve_speed(self.player1)
            y = self.get_serve_y_position(self.player1)
        else:
            dx, dy = self.get_serve_speed(self.player2, reverse=True)
            y = self.get_serve_y_position(self.player2)
        self.ball.reset(
            self.table.x,
            y + self.ball.radius * 2 * (1 if dy > 0 else -1),
            dx,
            dy
        )

    def get_serve_speed(self, player: Player, reverse: bool = False) -> tuple:
        dx = -self.ball.initial_dx if reverse else self.ball.initial_dx
        dy = self.ball.initial_dy
        if player.score % 2:
            dy = -dy
        return dx, dy

    def get_serve_y_position(self, player: Player) -> int:
        if player.score % 2:
            return self.table.lower_bound['top']
        else:
            return self.table.upper_bound['bottom']
