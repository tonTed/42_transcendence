import { handlerStartMenu } from './menu_handler.js'; 
import { handlerGameLoop } from './game_handler.js'; 
import { handlerNetwork } from './network.js';



document.addEventListener("DOMContentLoaded", function() {


    const canvas = document.getElementById('pongCanvas');
    const context = canvas.getContext('2d');

    console.log('pongCanvas', canvas);

    handlerStartMenu(canvas, context);
    handlerGameLoop();
    handlerNetwork(canvas, context);
});

export const loadCanvasGame = () => {
    const canvas = document.getElementById('pongCanvas');
    const context = canvas.getContext('2d');

    console.log('pongCanvas', canvas);

    handlerStartMenu(canvas, context);
    handlerGameLoop();
    handlerNetwork(canvas, context);
}