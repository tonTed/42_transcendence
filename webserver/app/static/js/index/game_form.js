import { getUsers } from "../api.js";

// Create the select element with user options
function createSelectElement(users) {
  const div = document.createElement("div");
  div.className = "row";

  const select = document.createElement("select");
  select.className = "form-select col mb-2 me-2 p-2";

  const defaultOption = document.createElement("option");
  defaultOption.selected = true;
  defaultOption.textContent = "Select a player";
  select.appendChild(defaultOption);

  users.forEach((user) => {
    const option = document.createElement("option");
    option.value = user.id;
    option.textContent = user.username;
    select.appendChild(option);
  });

  const input = document.createElement("input");
  input.type = "text";
  input.className = "form-control col mb-2 ms-2 p-2";
  input.placeholder = "Enter a player name";
  div.appendChild(select);
  div.appendChild(input);

  return div;
}

// Update the player select container based on the selected mode
function updateSelectPlayersContainer(users, selectedMode) {
  const selectPlayersContainer = document.getElementById(
    "select-players-container"
  );
  selectPlayersContainer.innerHTML = "";

  switch (selectedMode) {
    case "1v1":
      createMultipleSelectElements(selectPlayersContainer, users, 2);
      break;
    case "tournament":
      createMultipleSelectElements(selectPlayersContainer, users, 4);
      break;
    default:
      selectPlayersContainer.innerHTML = "<h1>No mode selected</h1>";
      break;
  }
}

// Create and add multiple player select elements
function createMultipleSelectElements(container, users, count) {
  for (let i = 0; i < count; i++) {
    container.appendChild(createSelectElement(users));
  }
}

// Update mode selection
function updateModeSelection(selectedButton, otherButton, mode, users) {
  selectedButton.classList.add("btn-success");
  otherButton.classList.remove("btn-success");
  updateSelectPlayersContainer(users, mode);
}

// Initialize the game form
export async function initGameForm() {
  const users = await getUsers();
  let selectedMode = null;

  const btn1v1 = document.getElementById("1v1");
  const btnTournament = document.getElementById("tournament");

  btn1v1.addEventListener("click", function () {
    updateModeSelection(btn1v1, btnTournament, "1v1", users);
  });

  btnTournament.addEventListener("click", function () {
    updateModeSelection(btnTournament, btn1v1, "tournament", users);
  });

  updateSelectPlayersContainer(users, selectedMode);
}
