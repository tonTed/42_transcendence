import asyncio
from .constants import BALL_CONSTS as B, PADDLE_CONSTS as PAD, CANVAS_CONSTS as C, GAME_CONSTS as G

class Paddle:
    def __init__(self, x, y, height, width, speed):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.velocity = 0
        self.speed = speed
        self.side = self.determine_playing_side()
        self.hitbox = self.calculate_hitbox()

    
    def update(self, keys_pressed, controls):
        self.update_velocity(keys_pressed, controls)
        self.move()

    def calculate_hitbox(self):
        return {
            'side': self.x if self.side == G.RIGHT_SIDE else self.x + self.width,
            'top' : self.y,
            'bottom' : self.y + self.height
        }
    
    def ball_offset(self, ball_y):
        return (ball_y - (self.y + self.height / 2))
    
    def determine_playing_side(self):
        return (self.x > C.CENTER_X)

    def update_velocity(self, keys_pressed, controls):
        self.velocity = 0
        if keys_pressed[controls['up']]:
            self.velocity -= self.speed
        if keys_pressed[controls['down']]:
            self.velocity += self.speed

    def move(self):
        self.y += self.velocity
        if self.is_out_of_bounds(C.HEIGHT, C.ORIGIN_Y):
            self.reset(C.HEIGHT, C.ORIGIN_Y)

    def is_out_of_bounds(self, lower_bound, upper_bound):
        self.hitbox = self.calculate_hitbox()
        return (self.hitbox['bottom'] > lower_bound or self.hitbox['top'] < upper_bound)

    def reset(self, lower_bound, upper_bound):
        if (self.hitbox['top'] < upper_bound):
            self.y = upper_bound
        else:
            self.y = lower_bound - self.height
    

class Ball:
    def __init__(self, x, y, radius, dx, dy):
        self.x = x
        self.y = y
        self.radius = radius
        self.dx = dx
        self.dy = dy
        self.hitbox = self.calculate_hitbox()

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def update(self, paddle1, paddle2, game):
        self.move()
        self.check_collision(paddle1, paddle2, game)

    def update_speed(self, dx, dy):
        self.dx = dx
        self.dy = dy

    def reset(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def calculate_hitbox(self):
        return {
            'left': self.x - self.radius,
            'right': self.x + self.radius,
            'top': self.y - self.radius,
            'bottom' : self.y + self.radius
        }
    
    def collision_with_boundaries(self, upper_boundary, bottom_boundary):
        return (self.y - self.radius <= upper_boundary or self.y + self.radius >= bottom_boundary)
    
    def collision_with_paddle(self, paddle):
        paddle_hitbox = paddle.calculate_hitbox()
        self.hitbox = self.calculate_hitbox()
        
        if paddle.side == G.RIGHT_SIDE:
            return (self.hitbox['right'] >= paddle_hitbox['side'] and
                    self.x <= paddle.x and
                    self.hitbox['bottom'] >= paddle_hitbox['top'] and
                    self.hitbox['top'] <= paddle_hitbox['bottom'])
        else:
            return (self.hitbox['left'] <= paddle_hitbox['side'] and
                    self.x >= paddle.x and
                    self.hitbox['bottom'] >= paddle_hitbox['top'] and
                    self.hitbox['top'] <= paddle_hitbox['bottom'])
    
    def check_collision(self, paddle1, paddle2, game):
        if (self.collision_with_paddle(paddle1)):
            self.update_speed(B.HIT_DX, paddle1.ball_offset(self.y) * B.COLLISION_COEFF)
            game.serve_state = False
        elif (self.collision_with_paddle(paddle2)):
            self.update_speed(-B.HIT_DX, paddle2.ball_offset(self.y) * B.COLLISION_COEFF)
            game.serve_state = False

        if game.serve_state == False and self.collision_with_boundaries(C.ORIGIN_Y, C.HEIGHT) :
            self.dy *= -1
    
class Player:
    def __init__(self, id, paddle_x):
        self.id = id
        self.paddle = Paddle(paddle_x, PAD.INITIAL_Y, PAD.HEIGHT, PAD.WIDTH, PAD.SPEED)
        self.score = 0
        self.controls = self.get_controls()
        self.goal = self.get_goal()
    
    def scored(self, ball_x):
        if self.paddle.side == G.LEFT_SIDE:
            return ball_x > self.goal
        return ball_x < self.goal

    def update_score(self):
        self.score += 1

    def get_controls(self):
        return {
            'up' : G.P1_UP_KEY if self.id == 1 else G.P2_UP_KEY,
            'down' : G.P1_DOWN_KEY if self.id == 1 else G.P2_DOWN_KEY
        }
    
    def get_goal(self):
        if (self.paddle.side == G.LEFT_SIDE):
            return C.WIDTH
        return C.ORIGIN_X

class Game:
    def __init__(self):
        self.player1 = Player(G.PLAYER1, PAD.PADDLE1_X)
        self.player2 = Player(G.PLAYER2, PAD.PADDLE2_X)
        self.ball = Ball(C.CENTER_X, C.ORIGIN_Y, B.RADIUS, B.INITIAL_DX, B.INITIAL_DY)
        self.keys_pressed = {
            G.P1_UP_KEY : False,
            G.P1_DOWN_KEY : False,
            G.P2_UP_KEY : False,
            G.P2_DOWN_KEY : False
        }
        self.resetting = True
        self.reset_task = asyncio.create_task(self.reset_game())
        self.winner = None
        self.winning_score = G.WINNING_SCORE
        self.serve_state= True
        self.last_scorer = None

    def update_key_states(self, keys_pressed):
        self.keys_pressed = keys_pressed

    def update(self):
        if not self.resetting:
            self.ball.update(self.player1.paddle, self.player2.paddle, self)
        self.update_paddles()
        if (self.reset_task is None or self.reset_task.done()) and self.player_scored():
            self.reset_task = asyncio.create_task(self.reset_game())

    def update_paddles(self):
        self.player1.paddle.update(self.keys_pressed, self.player1.controls)
        self.player2.paddle.update(self.keys_pressed, self.player2.controls)

    def is_winner_determined(self):
        if (self.player1.score >= self.winning_score):
                return self.player1.id
        elif (self.player2.score >= self.winning_score):
                return self.player2.id
        return None

    def player_scored(self):
        if self.player1.scored(self.ball.x):
            self.player1.update_score()
            self.last_scorer = self.player1.id
            return True
        elif self.player2.scored(self.ball.x):
            self.player2.update_score()
            self.last_scorer = self.player2.id
            return True
        self.winner = self.is_winner_determined()
        return False

    async def reset_game(self):
        self.resetting = True
        self.serve_state = True
        await asyncio.sleep(G.INTERVAL_TIME)
        self.serve()
        self.resetting = False

    def serve(self):
        if self.last_scorer == self.player1.id:
            dx, dy = B.INITIAL_DX, B.INITIAL_DY
            y = C.HEIGHT if self.player1.score % 2 else C.ORIGIN_Y
            dy = -dy if self.player1.score % 2 else dy
        else:
            dx, dy = -B.INITIAL_DX, B.INITIAL_DY
            y = C.HEIGHT if self.player2.score % 2 else C.ORIGIN_Y
            dy = -dy if self.player2.score % 2 else dy
        
        self.ball.reset(C.CENTER_X, y, dx, dy)

        
