from game.models.ball import Ball
from game.models.paddle import Paddle
from game.models.play_area import PlayArea


def _detect_collision(object1: dict, object2: dict) -> bool:
    return not (
        object1['right'] < object2['left'] or
        object1['left'] > object2['right'] or
        object1['top'] > object2['bottom'] or
        object1['bottom'] < object2['top']
    )


class CollisionHandler:
    def __init__(self, ball: 'Ball', paddle1: 'Paddle', paddle2: 'Paddle',
                 table: 'PlayArea') -> None:
        self.ball = ball
        self.paddle1 = paddle1
        self.paddle2 = paddle2
        self.table = table

    def ball_and_paddles(self) -> None:
        ball_hitbox = self.ball.get_hitbox()
        paddle1_hitbox = self.paddle1.get_hitbox()
        paddle2_hitbox = self.paddle2.get_hitbox()

        if _detect_collision(ball_hitbox, paddle1_hitbox):
            self.ball.update_speed(
                self.ball.hit_dx,
                (self.ball.y - self.paddle1.y) * self.ball.hit_coeff
            )
        elif _detect_collision(ball_hitbox, paddle2_hitbox):
            self.ball.update_speed(
                -self.ball.hit_dx,
                (self.ball.y - self.paddle2.y) * self.ball.hit_coeff
            )

    def ball_and_boundaries(self) -> None:
        ball_hitbox = self.ball.get_hitbox()

        if (_detect_collision(ball_hitbox, self.table.upper_bound) or
                _detect_collision(ball_hitbox, self.table.lower_bound)):
            self.ball.update_speed(self.ball.dx, -self.ball.dy)

    def paddles_and_boundaries(self) -> None:
        paddle1_hitbox = self.paddle1.get_hitbox()
        paddle2_hitbox = self.paddle2.get_hitbox()

        if _detect_collision(paddle1_hitbox, self.table.lower_bound):
            self.paddle1.reset(self.table.lower_bound['top'] -
                               self.paddle1.offset_y)
        elif _detect_collision(paddle1_hitbox, self.table.upper_bound):
            self.paddle1.reset(self.table.upper_bound['bottom'] +
                               self.paddle1.offset_y)

        if _detect_collision(paddle2_hitbox, self.table.lower_bound):
            self.paddle2.reset(self.table.lower_bound['top'] -
                               self.paddle2.offset_y)
        elif _detect_collision(paddle2_hitbox, self.table.upper_bound):
            self.paddle2.reset(self.table.upper_bound['bottom'] +
                               self.paddle2.offset_y)
