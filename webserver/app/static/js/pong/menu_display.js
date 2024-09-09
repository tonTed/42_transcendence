import { CANVAS, PLAY_BUTTON, PLAYERS } from './constants.js';
import { gameState } from './game_handler.js';
import { isMouseOverPlayButton } from './menu_handler.js';

export function clearCanvas(context, canvas) {
    context.clearRect(CANVAS.ORIGIN_X, CANVAS.ORIGIN_Y, canvas.width, canvas.height);
}

function drawPlayButton(canvas, context) {
    context.fillStyle = isMouseOverPlayButton(canvas, context) ? PLAY_BUTTON.HIGHLIGHT : PLAY_BUTTON.COLOR;
    context.font = `${PLAY_BUTTON.FONT_SIZE} "${PLAY_BUTTON.FONT}"`;
    context.textAlign = PLAY_BUTTON.TEXT_ALIGN;
    const textMetrics = context.measureText('START');
    const textHeight = textMetrics.actualBoundingBoxAscent + textMetrics.actualBoundingBoxDescent;
    const textWidth = textMetrics.width;
    context.fillText('START', PLAY_BUTTON.X , PLAY_BUTTON.Y + textHeight / 2);
}

function drawPlayersNames(canvas, context) {
    const player1 = gameState.players.p1Name;
    const player2 = gameState.players.p2Name;
    
    context.fillStyle = PLAYERS.COLOR;
    context.font = `${PLAYERS.FONT_SIZE} "${PLAYERS.FONT}"`;
    context.textAlign = PLAYERS.TEXT_ALIGN;
    
    context.fillText(player1, PLAYERS.PLAYER1_X , PLAYERS.PLAYER1_Y);
    context.fillText('vs.', CANVAS.CENTER_X , PLAYERS.PLAYER1_Y);
    context.fillText(player2, PLAYERS.PLAYER2_X , PLAYERS.PLAYER2_Y);
}

export function drawMenu(canvas, context) {
    clearCanvas(context, canvas);
    drawPlayButton(canvas, context);
    drawPlayersNames(canvas, context);
}