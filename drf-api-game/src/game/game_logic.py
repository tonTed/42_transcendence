import asyncio
from .constants import BALL_CONSTS as B, PADDLE_CONSTS as P, CANVAS_CONSTS as C, GAME_CONSTS as G

class Paddle:
    def __init__(self, x, y, height, width, velocity, speed):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.velocity = velocity
        self.speed = speed

    def move(self):
        self.y += self.velocity
        if self.y < C.ORIGIN_Y:
            self.y = C.ORIGIN_Y
        elif self.y + self.height > C.HEIGHT:
            self.y = C.HEIGHT - self.height

    def ball_offset(self, ball_y):
        return (ball_y - (self.y + self.height / 2))

class Ball:
    def __init__(self, x, y, radius, dx, dy):
        self.x = x
        self.y = y
        self.radius = radius
        self.dx = dx
        self.dy = dy

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def update_speed(self, dx, dy):
        self.dx = dx
        self.dy = dy

    def reset(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

class Game:
    def __init__(self):
        self.paddle1 = Paddle(P.PADDLE1_X, P.INITIAL_Y, P.HEIGHT, P.WIDTH, P.VELOCITY, P.SPEED)
        self.paddle2 = Paddle(P.PADDLE2_X, P.INITIAL_Y, P.HEIGHT, P.WIDTH, P.VELOCITY, P.SPEED)
        self.ball = Ball(C.CENTER_X, C.ORIGIN_Y, B.RADIUS, B.INITIAL_DX, B.INITIAL_DY)
        self.score1 = 0
        self.score2 = 0
        self.keys_pressed = {
            P.P1_UP_KEY : False,
            P.P1_DOWN_KEY : False,
            P.P2_UP_KEY : False,
            P.P2_DOWN_KEY : False
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
            self.ball.move()
            self.check_collision()
        self.update_paddles()
        if (self.reset_task is None or self.reset_task.done()) and self.check_score():
            self.reset_task = asyncio.create_task(self.reset_game())

    def update_paddle_velocity(self, paddle, up_key, down_key,):
        paddle.velocity = P.VELOCITY
        if self.keys_pressed[up_key] :
            paddle.velocity -= paddle.speed
        if self.keys_pressed[down_key] :
            paddle.velocity += paddle.speed

    def update_paddles(self):
        self.update_paddle_velocity(self.paddle1, P.P1_UP_KEY, P.P1_DOWN_KEY)
        self.update_paddle_velocity(self.paddle2, P.P2_UP_KEY, P.P2_DOWN_KEY)
        self.paddle1.move()
        self.paddle2.move()

    def collision_with_paddle(self, ball, paddle):
        return ( ball.x - ball.radius <= paddle.x + paddle.width and
            ball.x >= paddle.x and
            ball.y + ball.radius >= paddle.y and
            ball.y - ball.radius <= paddle.y + paddle.height)

    def collision_with_boundaries(self):
        return (self.ball.y - self.ball.radius <= C.ORIGIN_Y or self.ball.y + self.ball.radius >= C.HEIGHT)

    def check_collision(self):
        if (self.collision_with_paddle(self.ball, self.paddle1)):
            self.ball.update_speed(B.HIT_DX, self.paddle1.ball_offset(self.ball.y) * B.COLLISION_COEFF)
            self.serve_state = False
        elif (self.collision_with_paddle(self.ball, self.paddle2)):
            self.ball.update_speed(-B.HIT_DX, self.paddle2.ball_offset(self.ball.y) * B.COLLISION_COEFF)
            self.serve_state = False

        if self.serve_state == False and self.collision_with_boundaries() :
            self.ball.dy *= -1

    def player_scored(self, player):
        if player == 1:
            return self.ball.x > C.WIDTH
        return self.ball.x < C.ORIGIN_X

    def update_score(self, player):
        if player == 1:
            self.score1 += 1
            if (self.score1 >= self.winning_score):
                self.winner = G.PLAYER1
            self.last_scorer = G.PLAYER1
        else :
            self.score2 += 1
            self.last_scorer = G.PLAYER2
            if (self.score2 >= self.winning_score):
                self.winner = G.PLAYER2

    def check_score(self):
        if self.player_scored(G.PLAYER1):
            self.update_score(G.PLAYER1)
            return True
        elif self.player_scored(G.PLAYER2):
            self.update_score(G.PLAYER2)
            return True
        return False

    async def reset_game(self):
        self.resetting = True
        self.serve_state = True
        await asyncio.sleep(G.INTERVAL_TIME)
        self.serve()
        self.resetting = False

    def serve(self):
        if self.last_scorer == G.PLAYER1:
            dx, dy = B.INITIAL_DX, B.INITIAL_DY
            y = C.HEIGHT if self.score1 % 2 else C.ORIGIN_Y
            dy = -dy if self.score1 % 2 else dy
        else:
            dx, dy = -B.INITIAL_DX, B.INITIAL_DY
            y = C.HEIGHT if self.score2 % 2 else C.ORIGIN_Y
            dy = -dy if self.score2 % 2 else dy
        
        self.ball.reset(C.CENTER_X, y, dx, dy)

        
