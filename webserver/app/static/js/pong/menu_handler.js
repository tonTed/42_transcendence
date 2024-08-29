import { PLAY_BUTTON } from "./constants.js";
import { gameState } from "./game_handler.js";
import { drawMenu } from "./menu_display.js";
import { startGame } from "./network.js";
let mouseX, mouseY;

export async function handlerStartMenu(
  canvas,
  context,
  player1_name,
  player2_name,
  game_id
) {
  gameState.players.p1Name = player1_name;
  gameState.players.p2Name = player2_name;
  gameState.paused = false;

  function mouseMoveHandler(event) {
    const rect = canvas.getBoundingClientRect();
    mouseX = event.clientX - rect.left;
    mouseY = event.clientY - rect.top;
    if (!gameState.gameStarted) {
      drawMenu(canvas, context);
    }
  }

  const clickHandlerPromise = new Promise((resolve) => {
    async function clickHandler(event) {
      if (isMouseOverPlayButton(canvas, context)) {
        document.removeEventListener("mousemove", mouseMoveHandler);
        canvas.removeEventListener("click", clickHandler);
        const data = await startGame(canvas, context, game_id);
        resolve(data);
      }
    }
    canvas.addEventListener("click", clickHandler);
  });

  document.addEventListener("mousemove", mouseMoveHandler);

  document.fonts.ready.then(() => drawMenu(canvas, context));

  return await clickHandlerPromise;
}

export function isMouseOverPlayButton(canvas, context) {
  const textMetrics = context.measureText("START");
  const textHeight =
    textMetrics.actualBoundingBoxAscent + textMetrics.actualBoundingBoxDescent;
  const textWidth = textMetrics.width;
  const buttonLeft = PLAY_BUTTON.X - textWidth / 2;
  const buttonRight = PLAY_BUTTON.X + textWidth / 2;
  const buttonTop = PLAY_BUTTON.Y - textHeight / 2;
  const buttonBottom = PLAY_BUTTON.Y + textHeight / 2;

  return (
    mouseX >= buttonLeft &&
    mouseX <= buttonRight &&
    mouseY >= buttonTop &&
    mouseY <= buttonBottom
  );
}
