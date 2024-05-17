let mouseX, mouseY;
const PLAYBUTTONX = 400;
const PLAYBUTTONY = 300;

function handlerStartMenu(canvas, context) {
    document.addEventListener('mousemove', function(event) {
        const rect = canvas.getBoundingClientRect();
        mouseX = event.clientX - rect.left;
        mouseY = event.clientY - rect.top;
        if (!gameStarted) {
            drawPlayButton(canvas, context);
        }
    });

    canvas.addEventListener('click', function(event) {
        if (!gameStarted) {
            if (isMouseOverPlayButton(canvas, context)) {
                startGame();
            }
        }
    });

    document.fonts.ready.then(() => drawPlayButton(canvas, context));
}

function isMouseOverPlayButton(canvas, context) {
    const textMetrics = context.measureText('PLAY');
    const textHeight = textMetrics.actualBoundingBoxAscent + textMetrics.actualBoundingBoxDescent;
    const textWidth = textMetrics.width;
    const buttonLeft = PLAYBUTTONX - textWidth / 2;
    const buttonRight = PLAYBUTTONX + textWidth / 2;
    const buttonTop = PLAYBUTTONY - textHeight / 2;
    const buttonBottom = PLAYBUTTONY + textHeight / 2;

    return mouseX >= buttonLeft && mouseX <= buttonRight && mouseY >= buttonTop && mouseY <= buttonBottom;
}
