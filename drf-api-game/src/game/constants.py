class BALL_CONSTS:
    RADIUS = 9
    INITIAL_X = 400
    INITIAL_Y = 0
    INITIAL_DX = 1              # web: 5, cli: 1
    INITIAL_DY = 1              # web: 5, cli: 1
    HIT_DX = 1                  # web: 5, cli: 1
    COLLISION_COEFF = 0         # web: 0.25 cli: 0


class PADDLE_CONSTS:
    INITIAL_Y = 300
    HEIGHT = 80
    WIDTH = 10
    SPEED = 11
    PADDLE1_X = 12
    PADDLE2_X = 788


class CANVAS_CONSTS:
    WIDTH = 800
    HEIGHT = 600
    ORIGIN_X = 0
    ORIGIN_Y = 0


class GAME_CONSTS:
    FPS = 500
    WINNING_SCORE = 2
    PLAYER1 = 1
    PLAYER2 = 2
    INTERVAL_TIME = 1.5
    LEFT_SIDE = 0
    RIGHT_SIDE = 1
