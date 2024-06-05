import { handlerStartMenu } from './menu_handler.js'; 
import { handlerGameLoop } from './game_handler.js'; 
import { handlerNetwork } from './network.js';

export const loadCanvasGame = () => {
    const canvas = document.getElementById('pongCanvas');
    const context = canvas.getContext('2d');

    console.log('pongCanvas', canvas);

    handlerStartMenu(canvas, context);
    handlerGameLoop();
    handlerNetwork(canvas, context);
}