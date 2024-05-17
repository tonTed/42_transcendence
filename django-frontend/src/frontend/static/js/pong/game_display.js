function drawBall(context, ball_position, ball_radius) {
    context.beginPath();
    context.arc(ball_position.x, ball_position.y, ball_radius, 0, 2 * Math.PI);
    context.fill();
}

function drawPaddles(context, paddle1_position, paddle2_position, paddle_width, paddle_height) {
    context.fillRect(paddle1_position.x, paddle1_position.y, paddle_width, paddle_height);
    context.fillRect(paddle2_position.x, paddle2_position.y, paddle_width, paddle_height);
}

function drawWinner(context, canvas, winner, scores) {
    context.textAlign = 'center';
    context.fillText(`PLAYER ${winner} WINS`, canvas.width / 2, canvas.height / 2 - 20);
    context.fillText(`${scores.player1} - ${scores.player2}`, canvas.width / 2, canvas.height / 2 + 20);
}

function drawNet(context, canvas) {
    context.strokeStyle = '#fff';
    context.lineWidth = 2;
    context.setLineDash([12, 9]);
    context.beginPath();
    context.moveTo(canvas.width / 2, 0);
    context.lineTo(canvas.width / 2, canvas.height);
    context.stroke();
    context.setLineDash([]);
}

function drawScores(context, canvas, scores) {
    context.fillStyle = '#fff';
    if (scores.player1 < 10) {
        context.fillText(scores.player1, canvas.width / 4 - 15, 50);
    } else {
        context.fillText(scores.player1, canvas.width / 4 - 30, 50);
    }
    if (scores.player2 < 10) {
        context.fillText(scores.player2, (canvas.width / 4) * 3 - 15, 50);
    } else {
        context.fillText(scores.player2, (canvas.width / 4) * 3 - 30, 50);
    }
}

function drawGame(canvas, context, gameData) {
    clearCanvas(context, canvas);
    
    context.fillStyle = '#fff';
    context.font = '30px "Press Start 2P"';
    drawPaddles(context, gameData.paddle1_position, gameData.paddle2_position, gameData.paddle_width, gameData.paddle_height);
    if (gameIsInPlay(gameData)) {
        drawBall(context, gameData.ball_position, gameData.ball_radius);
    }
    if (winnerIsDecided(gameData)){
        drawWinner(context, canvas, gameData.winner, gameData.scores);
    } else {
        drawNet(context, canvas);
        drawScores(context, canvas, gameData.scores);
    }
    requestAnimationFrame(() => drawGame(canvas, context, gameData));
}
