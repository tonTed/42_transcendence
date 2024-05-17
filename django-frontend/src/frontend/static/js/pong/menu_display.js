function clearCanvas(context, canvas) {
    context.clearRect(0, 0, canvas.width, canvas.height);
}

function drawPlayButton(canvas, context) {
    clearCanvas(context, canvas);
    context.fillStyle = isMouseOverPlayButton(canvas, context) ? 'blue' : '#fff';
    context.font = '30px "Press Start 2P"';
    context.textAlign = 'center';
    const textMetrics = context.measureText('PLAY');
    const textHeight = textMetrics.actualBoundingBoxAscent + textMetrics.actualBoundingBoxDescent;
    const textWidth = textMetrics.width;
    context.fillText('PLAY', PLAYBUTTONX, PLAYBUTTONY + textHeight / 2);
}
