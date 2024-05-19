import asyncio
from sys import maxsize
from .constants import (
    BALL_CONSTS as BALL,
    PADDLE_CONSTS as PADDLE, 
    CANVAS_CONSTS as CANVAS,
    GAME_CONSTS as GAME,
    CONTROLS_CONSTS as CTRL)

class Paddle:
    def __init__(self, x: int, y: int, height: int, width: int, speed: int):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.velocity = 0
        self.speed = speed
        self.playing_side = self.determine_playing_side()
        self.hitbox = self.get_hitbox()

    def update(self, keys_pressed: dict, controls: dict) -> None:
        self.update_velocity(keys_pressed, controls)
        self.move()

    def get_hitbox(self) -> dict:
        return {
            'left': self.x,
            'right': self.x + self.width,
            'top' : self.y,
            'bottom' : self.y + self.height
        }
    
    def ball_offset(self, ball_y: int) -> float:
        return (ball_y - (self.y + self.height / 2))
    
    def determine_playing_side(self) -> bool:
        return (self.x > CANVAS.CENTER_X)

    def update_velocity(self, keys_pressed: dict, controls: dict) -> None:
        self.velocity = 0
        if keys_pressed[controls['up']]:
            self.velocity -= self.speed
        if keys_pressed[controls['down']]:
            self.velocity += self.speed

    def move(self) -> None:
        self.y += self.velocity
        if self.is_out_of_bounds(CANVAS.HEIGHT, CANVAS.ORIGIN_Y):
            self.reset(CANVAS.HEIGHT, CANVAS.ORIGIN_Y)

    def is_out_of_bounds(self, lower_bound: int, upper_bound: int) -> bool:
        self.hitbox = self.get_hitbox()
        return (self.hitbox['bottom'] > lower_bound or self.hitbox['top'] < upper_bound)

    def reset(self, lower_bound: int, upper_bound: int) -> None:
        self.y = upper_bound if self.hitbox['top'] < upper_bound else lower_bound - self.height
    

class Ball:
    def __init__(self, x: int, y: int, radius: int, dx: int, dy: int):
        self.x = x
        self.y = y
        self.radius = radius
        self.dx = dx
        self.dy = dy
        self.hitbox = self.get_hitbox()

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
    def __init__(self, id: int, paddle_x: int):
        self.id = id
        self.paddle = Paddle(paddle_x, PADDLE.INITIAL_Y, PADDLE.HEIGHT, PADDLE.WIDTH, PADDLE.SPEED)
        self.score = 0
        self.controls = self.get_controls()
        self.goal = self.get_goal()
    
    def scored(self, ball_x: int) -> bool:
        return ball_x > self.goal if self.paddle.playing_side == GAME.LEFT_SIDE else ball_x < self.goal

    def update_score(self) -> None:
        self.score += 1

    def get_controls(self) -> dict:
        return {
            'up' : CTRL.P1_UP_KEY if self.id == 1 else CTRL.P2_UP_KEY,
            'down' : CTRL.P1_DOWN_KEY if self.id == 1 else CTRL.P2_DOWN_KEY
        }
    
    def get_goal(self) -> int:
        return CANVAS.WIDTH if self.paddle.playing_side == GAME.LEFT_SIDE else CANVAS.ORIGIN_X

class Game:
    def __init__(self):
        self.player1 = Player(GAME.PLAYER1, PADDLE.PADDLE1_X)
        self.player2 = Player(GAME.PLAYER2, PADDLE.PADDLE2_X)
        self.ball = Ball(BALL.INITIAL_X, BALL.INITIAL_Y, BALL.RADIUS, BALL.INITIAL_DX, BALL.INITIAL_DY)
        self.keys_pressed = {
            self.player1.controls['up'] : False,
            self.player1.controls['down'] : False,
            self.player2.controls['up'] : False,
            self.player2.controls['down'] : False,
        }
        self.upper_bound = GAME.UPPER_BOUND
        self.lower_bound = GAME.LOWER_BOUND
        self.resetting = True
        self.reset_task = asyncio.create_task(self.reset_game())
        self.winner = None
        self.winning_score = GAME.WINNING_SCORE
        self.serve_state= True
        self.last_scorer = None

    def update_key_states(self, keys_pressed: dict) -> None:
        self.keys_pressed = keys_pressed

    def update(self) -> None:
        if not self.resetting:
            self.ball.update_position()
            self.check_collisions()
        self.update_paddles()
        if (self.reset_task is None or self.reset_task.done()) and self.player_scored():
            self.reset_task = asyncio.create_task(self.reset_game())

    def check_collision_ball_and_paddles(self, ball_hitbox: dict, paddle1_hitbox: dict, paddle2_hitbox: dict):
        if self.detect_collision(ball_hitbox, paddle1_hitbox):
            self.ball.update_speed(BALL.HIT_DX, self.player1.paddle.ball_offset(self.ball.y) * BALL.COLLISION_COEFF)
            self.serve_state = False
        elif self.detect_collision(ball_hitbox, paddle2_hitbox):
            self.ball.update_speed(-BALL.HIT_DX, self.player2.paddle.ball_offset(self.ball.y) * BALL.COLLISION_COEFF)
            self.serve_state = False

    def check_collision_ball_and_boundaries(self, ball_hitbox: dict, lower_hitbox: dict, upper_hitbox: dict):
        if not self.serve_state and (self.detect_collision(ball_hitbox, upper_hitbox) or 
                                    self.detect_collision(ball_hitbox, lower_hitbox)):
            self.ball.update_speed(self.ball.dx, -self.ball.dy)

    def check_collisions(self) -> None:
        ball_hitbox = self.ball.get_hitbox()
        paddle1_hitbox = self.player1.paddle.get_hitbox()
        paddle2_hitbox = self.player2.paddle.get_hitbox()

        self.check_collision_ball_and_paddles(ball_hitbox, paddle1_hitbox, paddle2_hitbox)
        self.check_collision_ball_and_boundaries(ball_hitbox, self.lower_bound, self.upper_bound)
            
    def detect_collision(self, object1: dict, object2: dict) -> bool:
        if object1['right'] < object2['left'] or object1['left'] > object2['right']:
            return False
        if object1['top'] > object2['bottom'] or object1['bottom'] < object2['top']:
            return False
        return True

    def update_paddles(self) -> None:
        self.player1.paddle.update(self.keys_pressed, self.player1.controls)
        self.player2.paddle.update(self.keys_pressed, self.player2.controls)

    def player_won(self, score: int) -> bool:
        return score > self.winning_score
        
    def player_scored(self) -> bool:
        if self.player1.scored(self.ball.x):
            self.player1.update_score()
            if self.player_won(self.player1.score):
                self.winner = self.player1.id
            return True
        elif self.player2.scored(self.ball.x):
            self.player2.update_score()
            if self.player_won(self.player2.score):
                self.winner = self.player2.id
            return True
        return False

    async def reset_game(self) -> None:
        self.resetting = True
        self.serve_state = True
        await asyncio.sleep(GAME.INTERVAL_TIME)
        self.serve()
        self.resetting = False

    def serve(self) -> None:
        if self.last_scorer == self.player1.id:
            dx, dy = self.get_serve_velocity(self.player1)
            y = self.get_serve_y_position(self.player1)
        else:
            dx, dy = self.get_serve_velocity(self.player2, reverse=True)
            y = self.get_serve_y_position(self.player2)
            
        self.ball.reset(CANVAS.CENTER_X, y, dx, dy)

    def get_serve_velocity(self, player: Player, reverse: bool = False) -> tuple:
        dx = -BALL.INITIAL_DX if reverse else BALL.INITIAL_DX
        dy = BALL.INITIAL_DY
        if player.score % 2:
            dy = -dy
        return dx, dy

    def get_serve_y_position(self, player: Player) -> int:
        return CANVAS.HEIGHT if player.score % 2 else CANVAS.ORIGIN_Y

        
