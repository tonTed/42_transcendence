import { createGame, createTournament } from "../api.js";

/**
 * @typedef {import("../types.js").Player} Player
 * @typedef {import("../types.js").Game} Game
 * @typedef {import("../types.js").Tournament} Tournament
 */

function displayGames(games) {
  console.log("displayGames");
  const container = document.getElementById("gameContainer");
  container.innerHTML = "";

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
    const player1 = game.player1.name ? game.player1.name : "TBD";
    const player2 = game.player2.name ? game.player2.name : "TBD";
    gameItem.innerHTML = `
      <th scope='row'>${index + 1}</th>
      <td><span class='${colorByStatus}'>${game.status}</span></td>
      <td class='text-center ${
        game.winner && game.winner === game.player1.id ? "text-bg-success" : ""
      }'>${player1}</td>
      <td class='text-center ${
        game.winner && game.winner === game.player2.id ? "text-bg-success" : ""
      }'>${player2}</td>
    `;
    tbody.appendChild(gameItem);
  });

  table.appendChild(thead);
  table.appendChild(tbody);
  container.appendChild(table);
}

/**
 * @param {Game} game
 */
async function launchGame(game) {
  console.log("launchGame", game);
}

/**
 * @param {Player[]} players
 */
async function manage1v1(players) {
  const response = await createGame(players);
  const games = response;
  launchGame(games[0]);
}

/**
 * @param {Player[]} players
 */
async function manageTournament(players) {
  const response = await createTournament(players);
  const games = response.games;
  displayGames(games);
}

/**
 * @param {Object} data
 * @param {string} data.mode - "1v1" | "tournament"
 * @param {Player[]} data.players - array of players
 */
async function gameManager(data) {
  if (data.mode === "1v1") {
    manage1v1(data.players);
  } else {
    manageTournament(data.players);
  }
}

export { gameManager };
