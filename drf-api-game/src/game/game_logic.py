import asyncio
from .constants import BALL_CONSTS as B, PADDLE_CONSTS as PAD, CANVAS_CONSTS as C, GAME_CONSTS as G

class Paddle:
    def __init__(self, x: int, y: int, height: int, width: int, speed: int):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.velocity = 0
        self.speed = speed
        self.side = self.determine_playing_side()
        self.hitbox = self.get_hitbox()

    def update(self, keys_pressed: dict, controls: dict) -> None:
        self.update_velocity(keys_pressed, controls)
        self.move()

    def get_hitbox(self) -> dict:
        return {
            'side': self.x if self.side == G.RIGHT_SIDE else self.x + self.width,
            'top' : self.y,
            'bottom' : self.y + self.height
        }
    
    def ball_offset(self, ball_y: int) -> float:
        return (ball_y - (self.y + self.height / 2))
    
    def determine_playing_side(self) -> bool:
        return (self.x > C.CENTER_X)

    def update_velocity(self, keys_pressed: dict, controls: dict) -> None:
        self.velocity = 0
        if keys_pressed[controls['up']]:
            self.velocity -= self.speed
        if keys_pressed[controls['down']]:
            self.velocity += self.speed

    def move(self) -> None:
        self.y += self.velocity
        if self.is_out_of_bounds(C.HEIGHT, C.ORIGIN_Y):
            self.reset(C.HEIGHT, C.ORIGIN_Y)

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

    def move(self) -> None:
        self.x += self.dx
        self.y += self.dy

    def update(self, paddle1: Paddle, paddle2: Paddle, game: 'Game') -> None:
        self.move()
        self.check_collision(paddle1, paddle2, game)

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
    
    def collision_with_boundaries(self, upper_boundary: int, bottom_boundary: int) -> bool:
        return (self.y - self.radius <= upper_boundary or self.y + self.radius >= bottom_boundary)
    
    def collision_with_paddle(self, paddle: Paddle) -> bool:
        paddle_hitbox = paddle.get_hitbox()
        self.hitbox = self.get_hitbox()
        
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
    
    def check_collision(self, paddle1: Paddle, paddle2: Paddle, game: 'Game') -> None:
        if (self.collision_with_paddle(paddle1)):
            self.update_speed(B.HIT_DX, paddle1.ball_offset(self.y) * B.COLLISION_COEFF)
            game.serve_state = False
        elif (self.collision_with_paddle(paddle2)):
            self.update_speed(-B.HIT_DX, paddle2.ball_offset(self.y) * B.COLLISION_COEFF)
            game.serve_state = False

        if game.serve_state == False and self.collision_with_boundaries(C.ORIGIN_Y, C.HEIGHT) :
            self.dy *= -1
    
class Player:
    def __init__(self, id: int, paddle_x: int):
        self.id = id
        self.paddle = Paddle(paddle_x, PAD.INITIAL_Y, PAD.HEIGHT, PAD.WIDTH, PAD.SPEED)
        self.score = 0
        self.controls = self.get_controls()
        self.goal = self.get_goal()
    
    def scored(self, ball_x: int) -> bool:
        return ball_x > self.goal if self.paddle.side == G.LEFT_SIDE else ball_x < self.goal

    def update_score(self, game: 'Game') -> None:
        self.score += 1
        game.last_scorer = self.id
        if self.score >= G.WINNING_SCORE:
            game.winner = self.id

    def get_controls(self) -> dict:
        return {
            'up' : G.P1_UP_KEY if self.id == 1 else G.P2_UP_KEY,
            'down' : G.P1_DOWN_KEY if self.id == 1 else G.P2_DOWN_KEY
        }
    
    def get_goal(self) -> int:
        return C.WIDTH if self.paddle.side == G.LEFT_SIDE else C.ORIGIN_X

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

    def update_key_states(self, keys_pressed: dict) -> None:
        self.keys_pressed = keys_pressed

    def update(self) -> None:
        if not self.resetting:
            self.ball.update(self.player1.paddle, self.player2.paddle, self)
        self.update_paddles()
        if (self.reset_task is None or self.reset_task.done()) and self.player_scored():
            self.reset_task = asyncio.create_task(self.reset_game())

    def update_paddles(self) -> None:
        self.player1.paddle.update(self.keys_pressed, self.player1.controls)
        self.player2.paddle.update(self.keys_pressed, self.player2.controls)

    def player_won(self, score: int) -> bool:
        return score >= G.WINNING_SCORE

    def player_scored(self) -> bool:
        if self.player1.scored(self.ball.x):
            self.player1.update_score(self)
            return True
        elif self.player2.scored(self.ball.x):
            self.player2.update_score(self)
            return True
        return False

    async def reset_game(self) -> None:
        self.resetting = True
        self.serve_state = True
        await asyncio.sleep(G.INTERVAL_TIME)
        self.serve()
        self.resetting = False

    def serve(self) -> None:
        if self.last_scorer == self.player1.id:
            dx, dy = self.get_serve_velocity(self.player1)
            y = self.get_serve_y_position(self.player1)
        else:
            dx, dy = self.get_serve_velocity(self.player2, reverse=True)
            y = self.get_serve_y_position(self.player2)
            
        self.ball.reset(C.CENTER_X, y, dx, dy)

    def get_serve_velocity(self, player: Player, reverse: bool = False) -> tuple:
        dx = -B.INITIAL_DX if reverse else B.INITIAL_DX
        dy = B.INITIAL_DY
        if player.score % 2:
            dy = -dy
        return dx, dy

    def get_serve_y_position(self, player: Player) -> int:
        return C.HEIGHT if player.score % 2 else C.ORIGIN_Y

        
