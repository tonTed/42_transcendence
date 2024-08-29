import { contentLoader } from "./index.js";
import { initGameForm } from "./game_form.js";

function getLeaderboard(games) {
  let winnerGame4, loserGame4, winnerGame3, loserGame3;

  if (games[3].winner_id === games[3].player1_id) {
    winnerGame4 = games[3].player1_name;
    loserGame4 = games[3].player2_name;
  } else {
    winnerGame4 = games[3].player2_name;
    loserGame4 = games[3].player1_name;
  }

  if (games[2].winner_id === games[2].player1_id) {
    winnerGame3 = games[2].player1_name;
    loserGame3 = games[2].player2_name;
  } else {
    winnerGame3 = games[2].player2_name;
    loserGame3 = games[2].player1_name;
  }

  return [winnerGame4, loserGame4, winnerGame3, loserGame3];
}

async function displayLeaderboard(games) {
  const container = document.getElementById("gameContainer");
  container.innerHTML = "";
  container.style.display = "flex";
  container.style.flexDirection = "column";

  const leaderboard = getLeaderboard(games);

  const list = document.createElement("ol");
  list.classList.add("list-group");
  list.classList.add("list-group-numbered");
  list.style.width = "75%";

  leaderboard.forEach((player) => {
    const listItem = document.createElement("li");
    listItem.classList.add("list-group-item");
    listItem.textContent = player;
    list.appendChild(listItem);
  });

  const button = document.createElement("button");
  button.textContent = "Back to website";
  button.classList.add("btn", "btn-primary", "mt-3");
  button.style.display = "block";
  button.style.margin = "0 auto";
  container.appendChild(button);

  container.appendChild(list);
  container.appendChild(button);

  await new Promise((resolve) => {
    button.addEventListener("click", () => {
      resolve();
    });
  });

  await contentLoader.load("form_game");
  initGameForm();
}

export { displayLeaderboard };
