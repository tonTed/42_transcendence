class Ball:
    def __init__(self, x: float, y: float, radius: float, dx: float, dy: float, 
                 hit_dx: float, hit_coeff: float):
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

    def update_speed(self, dx: float, dy: float) -> None:
        self.dx = dx
        self.dy = dy

    def reset(self, x: float, y: float, dx: float, dy: float) -> None:
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def get_hitbox(self) -> dict:
        return {
            'left': self.x - self.radius,
            'right': self.x + self.radius,
            'top': self.y - self.radius,
            'bottom': self.y + self.radius
        }
