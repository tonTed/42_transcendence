import { NET, CANVAS, SCORE, FINAL_SCORE, BALL_COLOR, PADDLES_COLOR } from "./constants.js";
import { clearCanvas } from './menu_display.js'
import { gameIsInPlay, winnerIsDecided } from './game_handler.js';

function drawBall(context, ball_position, ball_radius) {
    context.fillStyle = BALL_COLOR;
    context.beginPath();
    context.arc(ball_position.x, ball_position.y, ball_radius, 0, 2 * Math.PI);
    context.fill();
}

function drawPaddles(context, paddle1_position, paddle2_position, paddle_width, paddle_height) {
    context.fillStyle = PADDLES_COLOR;
    context.fillRect(paddle1_position.x, paddle1_position.y, paddle_width, paddle_height);
    context.fillRect(paddle2_position.x, paddle2_position.y, paddle_width, paddle_height);
}

function drawWinner(context, canvas, winner, scores) {
    context.fillStyle = FINAL_SCORE.COLOR;
    context.font = `${SCORE.FONT_SIZE} "${SCORE.FONT}"`;
    context.textAlign = FINAL_SCORE.TEXT_ALIGN;
    context.fillText(`PLAYER ${winner} WINS`, FINAL_SCORE.WINNER_X, FINAL_SCORE.WINNER_Y);
    context.fillText(`${scores.player1} - ${scores.player2}`, FINAL_SCORE.SCORE_X, FINAL_SCORE.SCORE_Y);
}

function drawNet(context, canvas) {
    context.strokeStyle = NET.COLOR;
    context.lineWidth = NET.WIDTH;
    context.setLineDash([NET.DASH_SIZE, NET.GAP_SIZE]);
    context.beginPath();
    context.moveTo(CANVAS.CENTER_X, CANVAS.ORIGIN_Y);
    context.lineTo(CANVAS.CENTER_X, canvas.height);
    context.stroke();
    context.setLineDash([]);
}

function drawScores(context, canvas, scores) {
    context.fillStyle = SCORE.COLOR;
    context.font = `${SCORE.FONT_SIZE} "${SCORE.FONT}"`;
    context.textAlign = SCORE.TEXT_ALIGN;
    context.fillText(scores.player1, SCORE.PLAYER1_X, SCORE.PLAYER1_Y);
    context.fillText(scores.player2, SCORE.PLAYER2_X, SCORE.PLAYER2_Y);
}

export function drawGame(canvas, context, gameData) {
    clearCanvas(context, canvas);
    
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
