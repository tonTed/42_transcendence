export const gameState = {
    keysPressed: {
        ArrowUp: false,
        ArrowDown: false,
        w: false,
        s: false
    },
    gameStarted: false
};

export function handlerGameLoop() {
    document.addEventListener('keydown', function(event) {
        if (event.key in gameState.keysPressed) {
            gameState.keysPressed[event.key] = true;
        }
    });

    document.addEventListener('keyup', function(event) {
        if (event.key in gameState.keysPressed) {
            gameState.keysPressed[event.key] = false;
        }
    });
}

export function gameIsInPlay(gameData){
    return (!gameData.resetting && !gameData.winner);
}

export function winnerIsDecided(gameData){
    return (gameData.winner);
}