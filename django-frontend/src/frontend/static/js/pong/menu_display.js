import { CANVAS, PLAY_BUTTON } from './constants.js';
import { isMouseOverPlayButton } from './menu_handler.js';

export function clearCanvas(context, canvas) {
    context.clearRect(CANVAS.ORIGIN_X, CANVAS.ORIGIN_Y, canvas.width, canvas.height);
}

export function drawPlayButton(canvas, context) {
    clearCanvas(context, canvas);
    context.fillStyle = isMouseOverPlayButton(canvas, context) ? PLAY_BUTTON.HIGHLIGHT : PLAY_BUTTON.COLOR;
    context.font = `${PLAY_BUTTON.FONT_SIZE} "${PLAY_BUTTON.FONT}"`;
    context.textAlign = PLAY_BUTTON.TEXT_ALIGN;
    const textMetrics = context.measureText('PLAY');
    const textHeight = textMetrics.actualBoundingBoxAscent + textMetrics.actualBoundingBoxDescent;
    const textWidth = textMetrics.width;
    context.fillText('PLAY', PLAY_BUTTON.X , PLAY_BUTTON.Y + textHeight / 2);
}
