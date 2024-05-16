document.addEventListener("DOMContentLoaded", function() {
    const canvas = document.getElementById('pongCanvas');
    const context = canvas.getContext('2d');

    const ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    const ws_path = ws_scheme + '://' + window.location.hostname + ':3002/ws/game/';
    const socket = new WebSocket(ws_path);

    let keysPressed = {
        ArrowUp: false,
        ArrowDown: false,
        w: false,
        s: false
    };

    socket.onopen = function(e) {
        console.log('WebSocket connection established');
    };

    socket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        drawGame(data);
    };

    socket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    function drawGame(gameData) {
        context.clearRect(0, 0, canvas.width, canvas.height);

        context.fillStyle = '#fff';
        context.beginPath();
        context.arc(gameData.ball_position.x, gameData.ball_position.y, 8, 0, 2 * Math.PI);
        context.fill();

        context.fillRect(5, gameData.paddle1_position.y, 10, 70);
        context.fillRect(780, gameData.paddle2_position.y, 10, 70);
    }

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

    setInterval(() => {
        socket.send(JSON.stringify({
            command: "keys",
            keysPressed: keysPressed
        }));
    }, 20); // Send key states every 50ms
});
