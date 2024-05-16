document.addEventListener("DOMContentLoaded", function() {
    const canvas = document.getElementById('pongCanvas');
    const context = canvas.getContext('2d');

    const ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    const ws_path = ws_scheme + '://' + window.location.hostname + ':3002/ws/game/';
    const socket = new WebSocket(ws_path);

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
        if (event.key === "ArrowUp" || event.key === "ArrowDown") {
            let step = event.key === "ArrowUp" ? -10 : 10;
            socket.send(JSON.stringify({ 
                command: "move",
                player_id: 2,
                step: step 
            }));
        } else if (event.key === "w" || event.key === "s") {
            let step = event.key === "w" ? -10 : 10;
            socket.send(JSON.stringify({ 
                command: "move",
                player_id: 1,
                step: step 
            }));
        }
    });
});
