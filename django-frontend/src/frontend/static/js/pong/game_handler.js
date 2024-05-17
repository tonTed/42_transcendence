let keysPressed = {
    ArrowUp: false,
    ArrowDown: false,
    w: false,
    s: false
};
let gameStarted = false;

function handlerGameLoop() {
    document.addEventListener('keydown', function(event) {
        if (event.key in keysPressed) {
            keysPressed[event.key] = true;
        }
    });

    document.addEventListener('keyup', function(event) {
        if (event.key in keysPressed) {
            keysPressed[event.key] = false;
        }
    });
}

function gameIsInPlay(gameData){
    return (!gameData.resetting && !gameData.winner);
}

function winnerIsDecided(gameData){
    return (gameData.winner);
}