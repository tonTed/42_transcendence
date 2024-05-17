import { gameState } from './game_handler.js';
import { drawGame } from './game_display.js';

let socket;

function sendKeyStates() {
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({
            command: "keys",
            keysPressed: gameState.keysPressed
        }));
    }
}

export function handlerNetwork(canvas, context) {
    const ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    const ws_path = ws_scheme + '://' + window.location.hostname + ':3002/ws/game/';

    window.startGame = function startGame() {
        socket = new WebSocket(ws_path);

        socket.onopen = function(e) {
            console.log('WebSocket connection established');
            setInterval(sendKeyStates, 1000 / 60);
        };

        socket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            drawGame(canvas, context, data);
        };

        socket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };

        gameState.gameStarted = true;
    };
}
