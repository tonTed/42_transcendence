import { contentLoader } from "./index.js";
import { initGameForm } from "./game_form.js";

function getLeaderboard(tournament_id) {
  return ["Teddy", "Asael", "Guillaume", "Gael"];
}

async function displayLeaderboard(tournament_id) {
  const container = document.getElementById("gameContainer");
  container.innerHTML = "";

  const leaderboard = getLeaderboard(tournament_id);

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

  container.appendChild(list);

  // TODO: Add button to go back to the form_game page
  await new Promise((resolve) => setTimeout(resolve, 5000));

  await contentLoader.load("form_game");
  initGameForm();
}

export { displayLeaderboard };
