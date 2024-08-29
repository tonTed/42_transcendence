import { handlerStartMenu } from "./menu_handler.js";
import { handlerGameLoop } from "./game_handler.js";
import { drawWinner } from "./game_display.js";
import { FINAL_SCORES_DURATION } from "./constants.js";
import { gameState } from "./game_handler.js";

async function displayGameEnded(context, canvas, data) {
  drawWinner(context, canvas, data.winner, data.scores);

  await new Promise((r) => setTimeout(r, FINAL_SCORES_DURATION));
  canvas.remove();
  gameState.gameStarted = false;
}

export const loadCanvasGame = async (game_id, player1_name, player2_name) => {
  const canvas = document.getElementById("pongCanvas");
  const context = canvas.getContext("2d");

  handlerGameLoop();
  const data = await handlerStartMenu(
    canvas,
    context,
    player1_name,
    player2_name,
    game_id
  );
  await displayGameEnded(context, canvas, data);
};
