from sys import maxsize


class PlayArea:
    def __init__(self, x: float, y: float, width: int, height: int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.left_goal = self.x - self.width / 2
        self.right_goal = self.x + self.width / 2
        self.upper_bound = {
            'top': -maxsize - 1,
            'bottom': self.y - self.height / 2,
            'left': self.left_goal,
            'right': self.right_goal
        }
        self.lower_bound = {
            'top': self.y + self.height / 2,
            'bottom': maxsize,
            'left': self.left_goal,
            'right': self.right_goal
        }
