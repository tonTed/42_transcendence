document.addEventListener("DOMContentLoaded", function() {
    const canvas = document.getElementById('pongCanvas');
    const context = canvas.getContext('2d');

    const ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    const ws_path = ws_scheme + '://' + window.location.hostname + ':3002/ws/game/';
    let socket;

    let keysPressed = {
        ArrowUp: false,
        ArrowDown: false,
        w: false,
        s: false
    };

    let gameStarted = false;
    let mouseX, mouseY;
    const playButtonWidth = 100;
    const playButtonHeight = 40;
    const playButtonX = canvas.width / 2;
    const playButtonY = canvas.height / 2;

    function drawPlayButton() {
        context.clearRect(0, 0, canvas.width, canvas.height);
        context.fillStyle = isMouseOverPlayButton() ? 'blue' : '#fff';
        context.font = '30px "Press Start 2P"';
        context.textAlign = 'center';
        const textMetrics = context.measureText('PLAY');
        const textHeight = textMetrics.actualBoundingBoxAscent + textMetrics.actualBoundingBoxDescent;
        const textWidth = textMetrics.width;
        context.fillText(`PLAY`, playButtonX, playButtonY + textHeight / 2);
    }

    function startGame() {
        socket = new WebSocket(ws_path);

        socket.onopen = function(e) {
            console.log('WebSocket connection established');
            setInterval(sendKeyStates, 1000 / 60); // Send key states 60 times per second
        };

        socket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            drawGame(data);
        };

        socket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };

        gameStarted = true;
    }

    function drawGame(gameData) {
        context.clearRect(0, 0, canvas.width, canvas.height);

        context.fillStyle = '#fff';

        if (!gameData.resetting && !gameData.winner) {
            context.beginPath();
            context.arc(gameData.ball_position.x, gameData.ball_position.y, gameData.ball_radius, 0, 2 * Math.PI);
            context.fill();
        }

        context.fillRect(gameData.paddle1_position.x, gameData.paddle1_position.y, gameData.paddle_width, gameData.paddle_height);
        context.fillRect(gameData.paddle2_position.x, gameData.paddle2_position.y, gameData.paddle_width, gameData.paddle_height);

        if (gameData.winner) {
            context.font = '25px "Press Start 2P"';
            context.textAlign = 'center';
            context.fillText(`PLAYER ${gameData.winner} WINS`, canvas.width / 2, canvas.height / 2 - 20);
            context.fillText(`${gameData.scores.player1} - ${gameData.scores.player2}`, canvas.width / 2, canvas.height / 2 + 20);
        } else {
            context.strokeStyle = '#fff';
            context.lineWidth = 2;
            context.setLineDash([12, 9]);
            context.beginPath();
            context.moveTo(canvas.width / 2, 0);
            context.lineTo(canvas.width / 2, canvas.height);
            context.stroke();
            context.setLineDash([]);

            context.font = '30px "Press Start 2P"';
            if (gameData.scores.player1 < 10) {
                context.fillText(gameData.scores.player1, canvas.width / 4 - 15, 50);
            } else {
                context.fillText(gameData.scores.player1, canvas.width / 4 - 30, 50);
            }
            if (gameData.scores.player2 < 10) {
                context.fillText(gameData.scores.player2, (canvas.width / 4) * 3 - 15, 50);
            } else {
                context.fillText(gameData.scores.player2, (canvas.width / 4) * 3 - 30, 50);
            }
        }

        requestAnimationFrame(() => drawGame(gameData)); // Schedule the next frame
    }

    function isMouseOverPlayButton() {
        const textMetrics = context.measureText('PLAY');
        const textHeight = textMetrics.actualBoundingBoxAscent + textMetrics.actualBoundingBoxDescent;
        const textWidth = textMetrics.width;
        const buttonLeft = playButtonX - textWidth / 2;
        const buttonRight = playButtonX + textWidth / 2;
        const buttonTop = playButtonY - textHeight / 2;
        const buttonBottom = playButtonY + textHeight / 2;

        return mouseX >= buttonLeft &&
               mouseX <= buttonRight &&
               mouseY >= buttonTop &&
               mouseY <= buttonBottom;
    }

    document.addEventListener('mousemove', function(event) {
        const rect = canvas.getBoundingClientRect();
        mouseX = event.clientX - rect.left;
        mouseY = event.clientY - rect.top;
        if (!gameStarted) {
            drawPlayButton();
        }
    });

    canvas.addEventListener('click', function(event) {
        if (!gameStarted) {
            if (isMouseOverPlayButton()) {
                startGame();
            }
        }
    });

    document.addEventListener('keydown', function(event) {
        if (event.key in keysPressed) {
            keysPressed[event.key] = true;
        }
    });

    document.addEventListener('keyup', function(event) {
        if (event.key in keysPressed) {
            keysPressed[event.key] = false;
        }
    });

    function sendKeyStates() {
        if (socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({
                command: "keys",
                keysPressed: keysPressed
            }));
        }
    }

    document.fonts.ready.then(drawPlayButton);
});
