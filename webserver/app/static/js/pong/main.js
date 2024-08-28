import { handlerStartMenu } from "./menu_handler.js";
import { handlerGameLoop } from "./game_handler.js";

export const loadCanvasGame = async (game_id, player1_name, player2_name) => {
  const canvas = document.getElementById("pongCanvas");
  const context = canvas.getContext("2d");

  await handlerStartMenu(canvas, context, player1_name, player2_name, game_id);
  handlerGameLoop();
};
