import { PLAY_BUTTON } from './constants.js';
import { isMouseOverPlayButton } from './menu_handler.js';

export function clearCanvas(context, canvas) {
    context.clearRect(0, 0, canvas.width, canvas.height);
}

export function drawPlayButton(canvas, context) {
    clearCanvas(context, canvas);
    context.fillStyle = isMouseOverPlayButton(canvas, context) ? 'blue' : '#fff';
    context.font = '30px "Press Start 2P"';
    context.textAlign = 'center';
    const textMetrics = context.measureText('PLAY');
    const textHeight = textMetrics.actualBoundingBoxAscent + textMetrics.actualBoundingBoxDescent;
    const textWidth = textMetrics.width;
    context.fillText('PLAY', PLAY_BUTTON.X , PLAY_BUTTON.Y + textHeight / 2);
}
