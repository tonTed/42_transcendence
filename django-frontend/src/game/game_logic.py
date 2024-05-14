class Paddle:
    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width

    def move(self, step):
        self.y += step

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
        self.paddle1 = Paddle(x=5, y=300, height=70, width=10)
        self.paddle2 = Paddle(x=780, y=300, height=70, width=10)
        self.ball = Ball(x=250, y=150, radius=8, dx=5, dy=5)
        self.score1 = 0
        self.score2 = 0

    def update(self):
        self.ball.move()

    def check_collision(self):
        if self.ball.x <= self.paddle1.x + self.paddle1.width and self.ball.y >= self.paddle1.y and self.ball.y <= self.paddle1.y + self.paddle1.height:
            self.ball.x = self.paddle1.x + self.paddle1.width + self.ball.radius
            self.ball.dx *= -1
            self.ball.dy = (self.ball.y - (self.paddle1.y + self.paddle1.height / 2)) / 4

        if self.ball.x + self.ball.radius >= self.paddle2.x and self.ball.y >= self.paddle2.y and self.ball.y <= self.paddle2.y + self.paddle2.height:
            self.ball.x = self.paddle2.x -self.ball.radius
            self.ball.dx *= -1
            self.ball.dy = (self.ball.y - (self.paddle2.y + self.paddle2.height / 2)) / 4

        if self.ball.y <= 0 or self.ball.y >= 600:
            self.ball.dy *= -1

    def update(self):
        self.ball.move()
        self.check_collision()

    def check_score(self):
        if self.ball.x < 0:
            self.score2 += 1
            self.reset_game()
        elif self.ball.x > 800:
            self.score1 += 1
            self.reset_game()

    def reset_game(self):
        self.ball = Ball(x=250, y=150, radius=10, dx=5, dy=5)

    def update(self):
        self.ball.move()
        self.check_collision()
        self.check_score()


