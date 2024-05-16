import asyncio

class Paddle:
    def __init__(self, x, y, height, width, speed):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.velocity = 0
        self.speed = speed

    def move(self):
        self.y += self.velocity
        if self.y < 0:
            self.y = 0
        elif self.y + self.height > 600:
            self.y = 600 - self.height

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

class Game:
    def __init__(self):
        self.paddle1 = Paddle(x=5, y=300, height=60, width=10, speed=10)
        self.paddle2 = Paddle(x=780, y=300, height=60, width=10, speed=10)
        self.ball = Ball(x=400, y=0, radius=6, dx=6, dy=7)
        self.score1 = 0
        self.score2 = 0
        self.keys_pressed = {
            "ArrowUp": False,
            "ArrowDown": False,
            "w": False,
            "s": False
        }
        self.resetting = False
        self.reset_task = None
        self.winner = None
        self.winning_score = 4

    def update_key_states(self, keys_pressed):
        self.keys_pressed = keys_pressed

    def update(self):
        if not self.resetting:
            self.ball.move()
        self.update_paddles()
        self.check_collision()
        if self.reset_task is None or self.reset_task.done():
            if self.check_score():
                self.reset_task = asyncio.create_task(self.reset_game())

    def update_paddles(self):
        if self.keys_pressed["w"] and not self.keys_pressed["s"]:
            self.paddle1.velocity = -self.paddle1.speed
        elif self.keys_pressed["s"] and not self.keys_pressed["w"]:
            self.paddle1.velocity = self.paddle1.speed
        else:
            self.paddle1.velocity = 0

        if self.keys_pressed["ArrowUp"] and not self.keys_pressed["ArrowDown"]:
            self.paddle2.velocity = -self.paddle2.speed
        elif self.keys_pressed["ArrowDown"] and not self.keys_pressed["ArrowUp"]:
            self.paddle2.velocity = self.paddle2.speed
        else:
            self.paddle2.velocity = 0

        self.paddle1.move()
        self.paddle2.move()

    def check_collision(self):
        if self.ball.x <= self.paddle1.x + self.paddle1.width and self.ball.y >= self.paddle1.y and self.ball.y <= self.paddle1.y + self.paddle1.height:
            self.ball.x = self.paddle1.x + self.paddle1.width + self.ball.radius
            self.ball.dx *= -1
            self.ball.dy = (self.ball.y - (self.paddle1.y + self.paddle1.height / 2)) / 2

        if self.ball.x + self.ball.radius >= self.paddle2.x and self.ball.y >= self.paddle2.y and self.ball.y <= self.paddle2.y + self.paddle2.height:
            self.ball.x = self.paddle2.x - self.ball.radius
            self.ball.dx *= -1
            self.ball.dy = (self.ball.y - (self.paddle2.y + self.paddle2.height / 2)) / 2

        if self.ball.y <= 0 or self.ball.y >= 600:
            self.ball.dy *= -1

    def check_score(self):
        if self.ball.x < 0:
            self.score2 += 1
            if (self.score2 >= self.winning_score):
                self.winner = 2
            return True
        elif self.ball.x > 800:
            self.score1 += 1
            if (self.score1 >= self.winning_score):
                self.winner = 1
            return True
        return False

    async def reset_game(self):
        self.resetting = True
        await asyncio.sleep(1.2)
        self.ball = Ball(x=400, y=0, radius=6, dx=6, dy=7)
        self.resetting = False
