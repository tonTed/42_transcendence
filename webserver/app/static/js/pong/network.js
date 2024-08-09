import { INTERVAL_DURATION } from "./constants.js";
import { gameState } from "./game_handler.js";
import { drawGame } from "./game_display.js";
import { contentLoader } from "../index/index.js";
import { initGameForm } from "../index/game_form.js";

let socket;

function sendActions() {
  if (socket.readyState === WebSocket.OPEN) {
    socket.send(
      JSON.stringify({
        command: "actions",
        actions: gameState.actions,
      })
    );
  }
}

async function displayGameEnded() {
  const canvas = document.getElementById("pongCanvas");
  canvas.remove();
  await contentLoader.load("form_game");
  initGameForm();
}

export function handlerNetwork(canvas, context) {
  const ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
  const ws_path = `${ws_scheme}://${window.location.hostname}:3002/ws/game/`;

  window.startGame = function startGame() {
    socket = new WebSocket(ws_path);

    socket.onopen = function (e) {
      console.debug("WebSocket connection established");
      setInterval(sendActions, INTERVAL_DURATION);
    };

    socket.onmessage = function (e) {
      const data = JSON.parse(e.data);
      drawGame(canvas, context, data);
    };

    socket.onclose = async function (e) {
      console.debug("WebSocket connection closed");
      await displayGameEnded();
    };

    gameState.gameStarted = true;
  };
}
