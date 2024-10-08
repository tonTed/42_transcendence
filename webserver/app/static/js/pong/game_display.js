import { NET, CANVAS, SCORE, FINAL_SCORE, BALL_COLOR, PADDLES_COLOR, PAUSE } from "./constants.js";
import { clearCanvas } from './menu_display.js'
import { gameIsInPlay, gameState, winnerIsDecided } from './game_handler.js';

let GAMEDATA = null;
let RUNNINGID = null;

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
    
    context.fillText(scores.player1, SCORE.SCORE1_X, SCORE.SCORE1_Y);
    context.fillText(scores.player2, SCORE.SCORE2_X, SCORE.SCORE2_Y);
    
    context.textAlign = SCORE.P1_TEXT_ALIGN;
    context.font = `${SCORE.P_FONT_SIZE} "${SCORE.FONT}"`;
    context.fillText(gameState.players.p1Name, SCORE.PLAYER1_X,SCORE.PLAYER1_Y);
    context.textAlign = SCORE.P2_TEXT_ALIGN;
    context.fillText(gameState.players.p2Name, SCORE.PLAYER2_X,SCORE.PLAYER2_Y);
}

function drawPause(context, canvas){
    context.fillStyle = PAUSE.COLOR;
    context.font = `${PAUSE.FONT_SIZE} "${PAUSE.FONT}"`;
    context.textAlign = PAUSE.TEXT_ALIGN;
    
    context.fillText(PAUSE.TEXT, PAUSE.X, PAUSE.Y);
    
    context.font = `${PAUSE.FONT_SIZE_BOTTOM_TEXT} "${PAUSE.FONT}"`;
    context.fillText(PAUSE.BOTTOM_TEXT, PAUSE.X, PAUSE.Y + PAUSE.BOTTOM_TEXT_OFFSET);
}

export function drawWinner(context, canvas, winner, scores) {
    const text = winner == 1 ? gameState.players.p1Name : gameState.players.p2Name
    clearCanvas(context, canvas);
    context.fillStyle = FINAL_SCORE.COLOR;
    context.font = `${SCORE.FONT_SIZE} "${SCORE.FONT}"`;
    context.textAlign = FINAL_SCORE.TEXT_ALIGN;
    context.fillText(`${text} WINS`, FINAL_SCORE.WINNER_X, FINAL_SCORE.WINNER_Y);
    context.fillText(`${scores.player1} - ${scores.player2}`, FINAL_SCORE.SCORE_X, FINAL_SCORE.SCORE_Y);
    cancelAnimationFrame(RUNNINGID);
    GAMEDATA = null;
}

export function updateData(canvas, context, gameData){
    if (!GAMEDATA){
        GAMEDATA = gameData;
        drawGame(canvas, context, gameData);
    }
    GAMEDATA = gameData;
}

export function drawGame(canvas, context, gameData) {
    clearCanvas(context, canvas);
    
    drawPaddles(context, gameData.paddle1_position, gameData.paddle2_position, gameData.paddle_width, gameData.paddle_height);
    if (gameIsInPlay(gameData)) {
        drawBall(context, gameData.ball_position, gameData.ball_radius);
    }
    if (!gameState.paused){
        drawNet(context, canvas);
    } else {
        drawPause(context, canvas);
    }
    drawScores(context, canvas, gameData.scores);
    
    RUNNINGID = requestAnimationFrame(() => drawGame(canvas, context, GAMEDATA));
}