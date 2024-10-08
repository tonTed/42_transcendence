import { createGame, createTournament, getGamesFromGamesIds } from "../api.js";
import { loadCanvasGame } from "../pong/main.js";
import { contentLoader } from "../index/index.js";
import { initGameForm } from "../index/game_form.js";
import { displayLeaderboard } from "./leaderboard.js";

/**
 * @typedef {import("../types.js").Player} Player
 * @typedef {import("../types.js").Game} Game
 * @typedef {import("../types.js").Tournament} Tournament
 */

function displayGames(games) {
  const container = document.getElementById("gameContainer");
  container.innerHTML = "";
  container.style.display = "flex";
  container.style.flexDirection = "column";

  const table = document.createElement("table");
  table.classList.add("table");
  table.style.width = "75%";
  table.style.border = "1px solid #000";
  table.style.margin = "0 auto";

  const thead = document.createElement("thead");
  const tbody = document.createElement("tbody");

  thead.innerHTML =
    "<tr class='table-dark'><th scope='col'>Game</th><th scope='col'>Status</th><th class='text-center' scope='col'>Player</th><th class='text-center' scope='col'>Player</th></tr>";

  games.forEach((game, index) => {
    let colorByStatus = "";
    switch (game.status) {
      case "not_started":
        colorByStatus = "badge text-bg-warning";
        break;
      case "in_progress":
        colorByStatus = "badge text-bg-info";
        break;
      case "finished":
        colorByStatus = "badge text-bg-success";
        break;
    }
    const gameItem = document.createElement("tr");
    const player1 = game.player1_name ? game.player1_name : "TBD";
    const player2 = game.player2_name ? game.player2_name : "TBD";
    gameItem.innerHTML = `
      <th scope='row'>${index + 1}</th>
      <td><span class='${colorByStatus}'>${game.status}</span></td>
      <td class='text-center ${
        game.winner_id && game.winner_id === game.player1_id
          ? "text-bg-success"
          : ""
      }'>${player1}</td>
      <td class='text-center ${
        game.winner_id && game.winner_id === game.player2_id
          ? "text-bg-success"
          : ""
      }'>${player2}</td>
    `;
    tbody.appendChild(gameItem);
  });

  table.appendChild(thead);
  table.appendChild(tbody);
  container.appendChild(table);

  const button = document.createElement("button");
  button.textContent = "Play Next Game";
  button.classList.add("btn", "btn-primary", "mt-3");
  button.style.display = "block";
  button.style.margin = "0 auto";
  container.appendChild(button);

  return button;
}

/**
 * @param {Game} game
 */
async function launchGame(game) {
  const gameContainer = document.getElementById("gameContainer");
  gameContainer.innerHTML = `<canvas id="pongCanvas" width="800" height="600" style="background: #000; display: block; margin: 0 auto"></canvas>`;
  await loadCanvasGame(game.id, game.player1_name, game.player2_name);
}

/**
 * @param {Player[]} players
 */
async function manage1v1(players) {
  const response = await createGame(players);
  const game = response;
  await launchGame(game);
}

/**
 * @param {Player[]} players
 */
async function manageTournament(players) {
  let response = await createTournament(players);
  let games = await getGamesFromGamesIds(response.games);
  for (let i = 0; i < games.length; i++) {
    const playNextButton = displayGames(games);
    await new Promise((resolve) => {
      playNextButton.addEventListener("click", () => {
        resolve();
      });
    });
    await launchGame(games[i]);
    games = await getGamesFromGamesIds(response.games);
  }
  await displayLeaderboard(games);
}

/**
 * @param {Object} data
 * @param {string} data.mode - "1v1" | "tournament"
 * @param {Player[]} data.players - array of players
 */
async function gameManager(data) {
  if (data.mode === "1v1") {
    await manage1v1(data.players);
  } else {
    await manageTournament(data.players);
  }
  await contentLoader.load("form_game");
  initGameForm();
}

export { gameManager };
