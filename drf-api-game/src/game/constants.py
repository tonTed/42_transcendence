class BALL_CONSTS:
    RADIUS = 30
    INITIAL_X = 400
    INITIAL_Y = 0
    INITIAL_DX = 4
    INITIAL_DY = 4
    HIT_DX = 8
    COLLISION_COEFF = 0.4

class PADDLE_CONSTS:
    INITIAL_Y = 300
    HEIGHT = 60
    WIDTH = 10
    SPEED = 11
    VELOCITY = 0
    PADDLE1_X = 5
    PADDLE2_X = 780
    P1_UP_KEY = 'w'
    P1_DOWN_KEY = 's'
    P2_UP_KEY = 'ArrowUp'
    P2_DOWN_KEY = 'ArrowDown'

class CANVAS_CONSTS:
    WIDTH = 800
    HEIGHT = 600
    ORIGIN_X = 0
    ORIGIN_Y = 0
    CENTER_X = 400

class GAME_CONSTS:
    FPS = 64
    WINNING_SCORE = 4
    PLAYER1 = 1
    PLAYER2 = 2
    INTERVAL_TIME = 1.5
