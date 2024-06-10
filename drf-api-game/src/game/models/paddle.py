class Paddle:
    def __init__(self, x: int, y: int, height: int, width: int, 
                 speed: int):
        self.x = x
        self.y = y
        self.offset_x = width / 2
        self.offset_y = height / 2
        self.width = width
        self.height = height
        self.velocity = 0
        self.speed = speed
        self.hitbox = self.get_hitbox()
        self.dy = 0

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
            'top': self.y - self.offset_y,
            'bottom': self.y + self.offset_y
        }