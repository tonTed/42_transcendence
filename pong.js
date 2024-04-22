const canvas = document.querySelector('canvas')
const ctx = canvas.getContext('2d')

canvas.width = 768
canvas.height = 576
var playersWidth = 10
var playersHeight = 70
var ballRadius = 8

class Sprite {
    constructor({pos, velocity, shape}) {
        this.pos = pos
        this.velocity = velocity
        this.shape = shape
    }

    draw() {
        ctx.fillStyle = 'white'
        if (this.shape == 'rect')
            ctx.fillRect(this.pos.x, this.pos.y, playersWidth, playersHeight)
        else if (this.shape == 'circle'){
            ctx.beginPath()
            ctx.arc(this.pos.x, this.pos.y, ballRadius, 0, Math.PI * 2, true)
            ctx.fill()
        }
    }

    update() {
        this.draw()
        this.pos.x += this.velocity.x
        this.pos.y += this.velocity.y
    }
}

const player1 = new Sprite({
    pos: {
        x: canvas.width - 5 - playersWidth,
        y: canvas.height / 2 - playersHeight / 2
    },
    velocity: {
        x: 0,
        y: 0
    },
    shape: 'rect'
})

const player2 = new Sprite({
    pos: {
        x: 5,
        y: canvas.height / 2 - playersHeight / 2
    },
    velocity: {
        x: 0,
        y: 0
    },
    shape: 'rect'
})

const ball = new Sprite({
    pos: {
        x: canvas.width / 2,
        y: canvas.height / 2
    },
    velocity: {
        x: 12,
        y: 0
    },
    shape: 'circle'
})

player1.draw();
player2.draw();
ball.draw();

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

function detectCollision(){
    if (player2.pos.x + playersWidth + ballRadius > ball.pos.x &&
        player2.pos.y + playersHeight > ball.pos.y &&
        player2.pos.y < ball.pos.y)
        return -1
    else if (player1.pos.x - ballRadius < ball.pos.x &&
        player1.pos.y + playersHeight > ball.pos.y &&
        player1.pos.y < ball.pos.y)
        return -1
    return 0

}

function animate() {
    window.requestAnimationFrame(animate)
    ctx.clearRect(0, 0, canvas.width, canvas.height)

    player1.update()
    player2.update()
    ball.update()
    player1.velocity.y = 0
    player2.velocity.y = 0

    //player1 movement
    if (keys.ArrowDown.pressed) {
        player1.velocity.y += 6
    }
    if (keys.ArrowUp.pressed){
        player1.velocity.y -= 6
    }
    //player2 movement
    if (keys.s.pressed) {
        player2.velocity.y += 6
    }
    if (keys.w.pressed){
        player2.velocity.y -= 6
    }
    //ball movement
    if (detectCollision())
        ball.velocity.x *= -1;
    if (ball.pos.x > canvas.width || ball.pos.x < 0){
        ball.pos.x = canvas.width / 2
        ball.pos.y = canvas.height / 2
    }
}

animate()

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
