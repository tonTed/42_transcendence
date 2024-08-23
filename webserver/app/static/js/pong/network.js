import { FINAL_SCORES_DURATION, INTERVAL_DURATION } from "./constants.js";
import { gameState } from "./game_handler.js";
import { updateData, drawWinner } from "./game_display.js";
import { contentLoader } from "../index/index.js";
import { initGameForm } from "../index/game_form.js";
import { getCookie } from "../utils.js";

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

async function displayGameEnded(context, canvas, data) {
  drawWinner(context, canvas, data.winner, data.scores);

  await new Promise((r) => setTimeout(r, FINAL_SCORES_DURATION));
  canvas.remove();
  gameState.gameStarted = false;
  await contentLoader.load("form_game");
  initGameForm();
  // TODO-GVAR: handle end of game and remove canvas
}

export function handlerNetwork(canvas, context, game_id) {
  let timer;
  const jwtToken = getCookie("jwt_token");
  const ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
  const ws_path = `${ws_scheme}://${window.location.hostname}/ws/game/?game_id=${game_id}&jwt=${jwtToken}`;
  window.startGame = function startGame() {
    socket = new WebSocket(ws_path);

    socket.onopen = function (e) {
      console.debug("WebSocket connection established");
      timer = setInterval(sendActions, INTERVAL_DURATION);
    };

    socket.onmessage = function (e) {
      const data = JSON.parse(e.data);
      if (data.state) {
        updateData(canvas, context, data.state);
      } else if (data.final) {
        clearInterval(timer);
        displayGameEnded(context, canvas, data.final);
      }
    };
    
    socket.onclose = async function (e) {
      console.debug("WebSocket connection closed");
    };

    gameState.gameStarted = true;
  };
}
