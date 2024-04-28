const canvas = document.querySelector('canvas')
const ctx = canvas.getContext('2d')

canvas.width = 768
canvas.height = 576
var paddleWidth = 10
var paddleHeight = 70
var ballRadius = 5
var ballStartVelocity = 3.5
var playerOffset = 8

class Player {
    constructor({pos, velocity}){
        this.pos = pos
        this.velocity = velocity
        this.score = 0
        this.height = paddleHeight
        this.width = paddleWidth
    }

    draw() {
        ctx.fillStyle = 'white'
        ctx.fillRect(this.pos.x, this.pos.y, paddleWidth, paddleHeight)
    }

    update() {
        this.draw()
        this.pos.y += this.velocity
    }
}

class Ball {
    constructor({pos, velocity}){
        this.pos = pos
        this.velocity = velocity
        this.radius = ballRadius
    }

    draw() {
        ctx.beginPath()
        ctx.arc(this.pos.x, this.pos.y, this.radius, 0, Math.PI * 2, true)
        ctx.fill()
    }

    update() {
        this.draw()
        this.pos.x += this.velocity.x
        this.pos.y += this.velocity.y
    }

    reset(scorer) {
        ball.pos.x = canvas.width / 2
        ball.pos.y = canvas.height / 2
        if (scorer == 1){
            ball.velocity.y = player1.score % 2 ? -0.3 : 0.3
            ball.velocity.x = -ballStartVelocity
        }
        else {
            ball.velocity.y = player2.score % 2 ? -0.3 : 0.3
            ball.velocity.x = ballStartVelocity
        }
    }

    detectBouncingCollision(){
        let x = 1
        let y = ball.velocity.y
        if (player2.pos.x + player2.width + ball.radius >= ball.pos.x &&
            player2.pos.y + player2.height >= ball.pos.y &&
            player2.pos.y <= ball.pos.y){
            ball.velocity.x = -8
            x = -1
            y = (ball.pos.y - (player2.pos.y + player2.height / 2)) / 4
        } else if (player1.pos.x - ball.radius <= ball.pos.x &&
            player1.pos.y + player1.height >= ball.pos.y &&
            player1.pos.y <= ball.pos.y){
            ball.velocity.x = 8
            x = -1
            y = (ball.pos.y - (player1.pos.y + player1.height / 2)) / 4
        } else if (ball.pos.y - ball.radius <= 0 || ball.pos.y + ball.radius >= canvas.height){
            y *= -1
        }
        return [x, y]
    }
}

class ScoreBoard {

    draw() {
        ctx.font = "50px Consolas";
        ctx.fillStyle = "white";
        ctx.fillText(`${player2.score}`, canvas.width /4 - 10, 50);
        ctx.fillText(`${player1.score}`, (canvas.width /4) * 3 - 15, 50);
    }
}

class Net {
    constructor(linesLen, width, gap){
        this.linesLen = linesLen
        this.gap = gap
        this.width = width
    }

    draw(){
        for (let pos = 2; pos < canvas.height; pos += this.linesLen + this.gap) {
            ctx.fillRect((canvas.width / 2) - (this.width / 2), pos, this.width, this.linesLen)
        }
    }
}

class Game {
    constructor() {
        this.interval = false
        this.pointsToWin = 3
        this.finished = false
        this.winner = 0
    }
    startInterval(){
        this.interval = true
        setTimeout(() => this.endInterval(), 700)
    }
    endInterval(){
        this.interval = false
    }
    scorePoint(scorer){
        if (scorer === 1) {
            player1.score++
        } else {
            player2.score++
        }
        ball.reset(scorer)
        if (player1.score >= this.pointsToWin || player2.score >= this.pointsToWin){
            this.finished = true
            this.winner = player1.score > player2.score ? 1 : 2
        } else {
            this.startInterval()
        }
    }
    showResults(){
        ctx.font = "50px Consolas";
        ctx.fillStyle = "white";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(`PLAYER ${this.winner} WINS!`, canvas.width / 2, canvas.height / 2 - 50);
        ctx.fillText(`${player2.score} - ${player1.score}`, canvas.width /2, canvas.height / 2 + 20);
    }
}

const player1 = new Player({
    pos: {
        x: canvas.width - playerOffset - paddleWidth,
        y: canvas.height / 2 - paddleHeight / 2
    },
    velocity: 0
})

const player2 = new Player({
    pos: {
        x: playerOffset,
        y: canvas.height / 2 - paddleHeight / 2
    },
    velocity: 0
})

const ball = new Ball({
    pos: {
        x: canvas.width / 2,
        y: canvas.height / 2
    },
    velocity: {
        x: ballStartVelocity,
        y: -0.3
    }
})

const scoreBoard = new ScoreBoard()
const net = new Net(20, 2, 5)
const game = new Game()

const   keys = {
    ArrowUp: {
        pressed: false
    },
    ArrowDown: {
        pressed: false
    },
    w: {
        pressed: false
    },
    s: {
        pressed: false
    }
}

player1.draw()
player2.draw()
ball.draw()
scoreBoard.draw()
net.draw()
animate()

function handlePlayerMovement(){
    player1.velocity = 0
    player2.velocity = 0
    // player 1 movement
    if (keys.ArrowDown.pressed && (player1.pos.y + paddleHeight) < canvas.height) {
    player1.velocity += 8
    }
    if (keys.ArrowUp.pressed && player1.pos.y > 0){
        player1.velocity -= 8
    }
    //player2 movement
    if (keys.s.pressed && (player2.pos.y + paddleHeight) < canvas.height) {
        player2.velocity += 8
    }
    if (keys.w.pressed && player2.pos.y > 0){
        player2.velocity -= 8
    }
}

function handleBallMovement() {
    const values = ball.detectBouncingCollision()
    ball.velocity.x *= values[0]
    ball.velocity.y = values[1]
    if (ball.pos.x > canvas.width){
        game.scorePoint(2)
    } else if (ball.pos.x < 0){
        game.scorePoint(1)
    }
}

function animate() {
    window.requestAnimationFrame(animate)
    ctx.clearRect(0, 0, canvas.width, canvas.height)

    player1.update()
    player2.update()    
    if (game.finished == true){
        game.showResults()
    } else {
        if (game.interval == false)
            ball.update()
        scoreBoard.draw()
        net.draw()
    }
    if (game.finished == false){
        handlePlayerMovement()
        handleBallMovement()
    }
}


window.addEventListener('keydown', (event) => {
    switch (event.key){
        case 'ArrowUp':
            keys.ArrowUp.pressed = true
            break;
        case 'ArrowDown':
            keys.ArrowDown.pressed = true
            break;
        case 'w':
            keys.w.pressed = true
            break;
        case 's':
            keys.s.pressed = true
            break;
    }
})

window.addEventListener('keyup', (event) => {
    switch (event.key){
        case 'ArrowUp':
            keys.ArrowUp.pressed = false
            break;
        case 'ArrowDown':
            keys.ArrowDown.pressed = false
            break;
        case 'w':
            keys.w.pressed = false
            break;
        case 's':
            keys.s.pressed = false
            break;
    }
})
