import { handlerStartMenu } from "./menu_handler.js";
import { handlerGameLoop } from "./game_handler.js";
import { handlerNetwork } from "./network.js";

export const loadCanvasGame = (game_id, player1_name, player2_name) => {
  const canvas = document.getElementById("pongCanvas");
  const context = canvas.getContext("2d");

  handlerStartMenu(canvas, context, player1_name, player2_name);
  handlerGameLoop();
  handlerNetwork(canvas, context, game_id);
};
