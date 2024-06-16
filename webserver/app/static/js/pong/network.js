import { INTERVAL_DURATION } from './constants.js'
import { gameState } from './game_handler.js';
import { drawGame } from './game_display.js';

let socket;

function sendActions() {
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({
            command: "actions",
            actions: gameState.actions
        }));
    }
}

export function handlerNetwork(canvas, context) {
    const ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    const ws_path = ws_scheme + '://' + window.location.hostname + ':3002/ws/game/';

    window.startGame = function startGame() {
        socket = new WebSocket(ws_path);

        socket.onopen = function(e) {
            console.debug('WebSocket connection established');
            setInterval(sendActions, INTERVAL_DURATION);
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
