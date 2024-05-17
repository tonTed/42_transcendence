document.addEventListener("DOMContentLoaded", function() {
    const canvas = document.getElementById('pongCanvas');
    const context = canvas.getContext('2d');

    handlerStartMenu(canvas, context);
    handlerGameLoop();
    initializeNetwork(canvas, context);
});
