document.addEventListener("DOMContentLoaded", function() {
    const canvas = document.getElementById('pongCanvas');
    const context = canvas.getContext('2d');

    initializeGame(canvas, context);
    initializeNetwork(canvas, context);
});
