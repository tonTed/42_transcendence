import { INTERVAL_DURATION } from "./constants.js";
import { gameState } from "./game_handler.js";
import { updateData } from "./game_display.js";
import { getCookie } from "../utils.js";

let socket;

function sendActions() {
  if (socket.readyState === WebSocket.OPEN) {
    if (gameState.paused) {
      socket.send(
        JSON.stringify({
          command: "pause",
        })
      );
    } else {
      socket.send(
        JSON.stringify({
          command: "actions",
          actions: gameState.actions,
        })
      );
    }
  }
}

export async function startGame(canvas, context, game_id) {
  const jwtToken = getCookie("jwt_token");
  const ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
  const ws_path = `${ws_scheme}://${window.location.hostname}/ws/game/?game_id=${game_id}&jwt=${jwtToken}`;

  let finalData;

  let timer;
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
      finalData = data.final;
    }
  };

  const socketClosePromise = new Promise((resolve) => {
    socket.onclose = function (e) {
      console.debug("WebSocket connection closed");
      resolve(finalData);
    };
  });

  gameState.gameStarted = true;

  const data = await socketClosePromise;
  return data;
}
