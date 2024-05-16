function initializeNetwork(canvas, context) {
    const ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    const ws_path = ws_scheme + '://' + window.location.hostname + ':3002/ws/game/';
    let socket;

    window.startGame = function startGame() {
        socket = new WebSocket(ws_path);

        socket.onopen = function(e) {
            console.log('WebSocket connection established');
            setInterval(sendKeyStates, 1000 / 60); // Send key states 60 times per second
        };

        socket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            drawGame(canvas, context, data);
        };

        socket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };

        gameStarted = true;
    };

    function sendKeyStates() {
        if (socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({
                command: "keys",
                keysPressed: keysPressed
            }));
        }
    }
}
