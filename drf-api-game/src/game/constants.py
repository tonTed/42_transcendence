class BALL_CONSTS_WEB:
    RADIUS = 8
    INITIAL_X = 400
    INITIAL_Y = 0
    INITIAL_DX = 5
    INITIAL_DY = 5
    HIT_DX = 7
    COLLISION_COEFF = 0.25


class BALL_CONSTS_CLI:
    RADIUS = 9
    INITIAL_X = 400
    INITIAL_Y = 0
    INITIAL_DX = 1
    INITIAL_DY = 1
    HIT_DX = 1
    COLLISION_COEFF = 0


class BALL_CONSTS(BALL_CONSTS_WEB):
    pass


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
    FPS = 64
    WINNING_SCORE = 3
    PLAYER1 = 1
    PLAYER2 = 2
    INTERVAL_TIME = 2.5
    LEFT_SIDE = 0
    RIGHT_SIDE = 1
