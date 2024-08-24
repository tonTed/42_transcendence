export const gameState = {
    actions: {
        p1Up: false,
        p1Down: false,
        p2Up: false,
        p2Down: false,
    },
    gameStarted: false,
    players: {
        p1Name: null,
        p2Name: null
    },
    paused: false
};

const keyToActionMap = {
    'w': 'p1Up',
    's': 'p1Down',
    'ArrowUp': 'p2Up',
    'ArrowDown': 'p2Down'
};

export function handlerGameLoop() {
    document.addEventListener('keydown', function(event) {
        if (event.key == 'Escape'){
            gameState.paused = !gameState.paused;
            return;
        }
        if (!gameState.paused){
            const action = keyToActionMap[event.key];
            if (action) {
                gameState.actions[action] = true;
            }
        }
    });

    document.addEventListener('keyup', function(event) {
        const action = keyToActionMap[event.key];
        if (action) {
            gameState.actions[action] = false;
        }
    });
}

export function gameIsInPlay(gameData){
    return (!gameData.resetting && !gameData.winner);
}

export function winnerIsDecided(gameData){
    return (gameData.winner);
}
