import asyncio
from .constants import (
    BALL_CONSTS as BALL,
    PADDLE_CONSTS as PADDLE, 
    CANVAS_CONSTS as CANVAS,
    GAME_CONSTS as GAME,
    CONTROLS_CONSTS as CTRL)
from sys import maxsize

class Paddle:
    def __init__(self, x: int, y: int, height: int, width: int, speed: int):
        self.x = x
        self.y = y
        self.offset_x = width / 2
        self.offset_y = height / 2
        self.width = width
        self.height = height
        self.velocity = 0
        self.speed = speed
        self.hitbox = self.get_hitbox()

    def update_position(self, keys_pressed: dict, controls: dict) -> None:
        self.update_velocity(keys_pressed, controls)
        self.move()

    def update_velocity(self, keys_pressed: dict, controls: dict) -> None:
        self.velocity = 0
        if keys_pressed[controls['up']]:
            self.velocity -= self.speed
        if keys_pressed[controls['down']]:
            self.velocity += self.speed

    def move(self) -> None:
        self.y += self.velocity

    def reset(self, y: int) -> None:
        self.y = y
        self.dy = 0
        
    def get_hitbox(self) -> dict:
        return {
            'left': self.x - self.offset_x,
            'right': self.x + self.offset_x,
            'top' : self.y - self.offset_y,
            'bottom' : self.y + self.offset_y
        }
    

class Ball:
    def __init__(self, x: int, y: int, radius: int, dx: int, dy: int, hit_dx: int, hit_coeff: float):
        self.x = x
        self.y = y
        self.radius = radius
        self.dx = dx
        self.dy = dy
        self.initial_dx = dx
        self.initial_dy = dy
        self.hit_dx = hit_dx
        self.hit_coeff = hit_coeff

    def update_position(self) -> None:
        self.x += self.dx
        self.y += self.dy

    def update_speed(self, dx: int, dy: int) -> None:
        self.dx = dx
        self.dy = dy

    def reset(self, x: int, y: int, dx: int, dy: int) -> None:
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def get_hitbox(self) -> dict:
        return {
            'left': self.x - self.radius,
            'right': self.x + self.radius,
            'top': self.y - self.radius,
            'bottom' : self.y + self.radius
        }
    
class Player:
    def __init__(self, id: int, paddle_x: int, goal: int) -> None:
        self.id = id
        self.paddle = Paddle(paddle_x, PADDLE.INITIAL_Y, PADDLE.HEIGHT, PADDLE.WIDTH, PADDLE.SPEED)
        self.score = 0
        self.controls = self.get_controls()
        self.goal = goal
        self.playing_side = (self.paddle.x > self.goal)
    
    def scored(self, ball_x: int) -> bool:
        return ball_x > self.goal if self.playing_side == GAME.LEFT_SIDE else ball_x < self.goal

    def update_score(self) -> None:
        self.score += 1

    def get_controls(self) -> dict:
        return {
            'up' : CTRL.P1_UP_KEY if self.id == 1 else CTRL.P2_UP_KEY,
            'down' : CTRL.P1_DOWN_KEY if self.id == 1 else CTRL.P2_DOWN_KEY
        }

class Table:
    def __init__(self, x: float, y: float, width: int, height: int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.left_goal = self.x - self.width / 2
        self.right_goal = self.x + self.width / 2
        self.upper_bound = {
            'top'   : -maxsize - 1,
            'bottom': self.y - self.height / 2,
            'left'  : self.left_goal,
            'right' : self.right_goal
        }
        self.lower_bound = {
            'top'    : self.y + self.height / 2,
            'bottom' : maxsize,
            'left'   : self.left_goal,
            'right'  : self.right_goal
        }

class CollisionHandler:
    def detect_collision(self, object1: dict, object2: dict) -> bool:
        return not (
            object1['right'] < object2['left'] or
            object1['left'] > object2['right'] or
            object1['top'] > object2['bottom'] or
            object1['bottom'] < object2['top']
        )

    def check_collision_ball_and_paddles(self, ball: 'Ball', paddle1: 'Paddle', paddle2: 'Paddle') -> None:
        ball_hitbox = ball.get_hitbox()
        paddle1_hitbox = paddle1.get_hitbox()
        paddle2_hitbox = paddle2.get_hitbox()

        if self.detect_collision(ball_hitbox, paddle1_hitbox):
            ball.update_speed(ball.hit_dx, (ball.y - paddle1.y) * ball.hit_coeff)
        elif self.detect_collision(ball_hitbox, paddle2_hitbox):
            ball.update_speed(-ball.hit_dx, (ball.y - paddle2.y) * ball.hit_coeff)

    def check_collision_ball_and_boundaries(self, ball: 'Ball', table: 'Table') -> None:
        ball_hitbox = ball.get_hitbox()

        if self.detect_collision(ball_hitbox, table.upper_bound) or self.detect_collision(ball_hitbox, table.lower_bound):
            ball.update_speed(ball.dx, -ball.dy)

    def check_collision_paddles_and_boundaries(self, paddle1: 'Paddle', paddle2: 'Paddle', table: 'Table') -> None:
        paddle1_hitbox = paddle1.get_hitbox()
        paddle2_hitbox = paddle2.get_hitbox()

        if self.detect_collision(paddle1_hitbox, table.lower_bound):
            paddle1.reset(table.lower_bound['top'] - paddle1.offset_y)
        elif self.detect_collision(paddle1_hitbox, table.upper_bound):
            paddle1.reset(table.upper_bound['bottom'] + paddle1.offset_y)
        
        if self.detect_collision(paddle2_hitbox, table.lower_bound):
            paddle2.reset(table.lower_bound['top'] - paddle2.offset_y)
        elif self.detect_collision(paddle2_hitbox, table.upper_bound):
            paddle2.reset(table.upper_bound['bottom'] + paddle2.offset_y)

class Game:
    def __init__(self) -> None:
        self.table = Table(CANVAS.WIDTH / 2, CANVAS.HEIGHT / 2, CANVAS.WIDTH, CANVAS.HEIGHT)
        self.player1 = Player(GAME.PLAYER1, PADDLE.PADDLE1_X, self.table.right_goal)
        self.player2 = Player(GAME.PLAYER2, PADDLE.PADDLE2_X, self.table.left_goal)
        self.ball = Ball(BALL.INITIAL_X, BALL.INITIAL_Y, BALL.RADIUS, BALL.INITIAL_DX, BALL.INITIAL_DY, BALL.HIT_DX, BALL.COLLISION_COEFF)
        self.keys_pressed = {
            self.player1.controls['up'] : False,
            self.player1.controls['down'] : False,
            self.player2.controls['up'] : False,
            self.player2.controls['down'] : False,
        }
        self.resetting = True
        self.reset_time = GAME.INTERVAL_TIME
        self.reset_task = asyncio.create_task(self.reset_game())
        self.winner = None
        self.winning_score = GAME.WINNING_SCORE
        self.last_scorer = self.player2.id
        self.collision_handler = CollisionHandler()

    def update_key_states(self, keys_pressed: dict) -> None:
        self.keys_pressed = keys_pressed

    def update(self) -> None:
        self.ball.update_position()
        self.player1.paddle.update_position(self.keys_pressed, self.player1.controls)
        self.player2.paddle.update_position(self.keys_pressed, self.player2.controls)
        self.check_collisions()
        if (self.reset_task is None or self.reset_task.done()) and self.player_scored():
            self.reset_task = asyncio.create_task(self.reset_game())

    def check_collisions(self) -> None:
        self.collision_handler.check_collision_ball_and_paddles(self.ball, self.player1.paddle, self.player2.paddle)
        self.collision_handler.check_collision_ball_and_boundaries(self.ball, self.table)
        self.collision_handler.check_collision_paddles_and_boundaries(self.player1.paddle, self.player2.paddle, self.table)
            
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
            dx, dy = self.get_serve_velocity(self.player1)
            y = self.get_serve_y_position(self.player1)
        else:
            dx, dy = self.get_serve_velocity(self.player2, reverse=True)
            y = self.get_serve_y_position(self.player2)
        self.ball.reset(self.table.x, y + self.ball.radius * 2 * (1 if dy > 0 else -1), dx, dy)

    def get_serve_velocity(self, player: Player, reverse: bool = False) -> tuple:
        dx = -self.ball.initial_dx if reverse else self.ball.initial_dx
        dy = self.ball.initial_dy
        if player.score % 2:
            dy = -dy
        return dx, dy

    def get_serve_y_position(self, player: Player) -> int:
        return self.table.lower_bound['top'] if player.score % 2 else self.table.upper_bound['bottom']

