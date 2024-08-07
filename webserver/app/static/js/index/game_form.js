import { getUsers } from "../api.js";

// Create the select element with user options
function createSelectElement(users) {
  const div = document.createElement("div");
  div.className = "row";

  const select = document.createElement("select");
  select.className = "form-select col mb-2 me-2 p-2";
  select.required = true;

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
  input.required = true;

  div.appendChild(select);
  div.appendChild(input);

  // Add the selected option's text content to the input field
  select.addEventListener("change", function () {
    input.value = select.options[select.selectedIndex].textContent;
  });

  return div;
}

// Validate the form inputs
function validateForm() {
  const selectPlayersContainer = document.getElementById(
    "select-players-container"
  );
  const selectElements = selectPlayersContainer.querySelectorAll("select");
  const inputElements = selectPlayersContainer.querySelectorAll("input");

  // Check if all select elements have a numeric value
  for (const select of selectElements) {
    if (isNaN(select.value)) {
      return "An input element is not selected";
    }
  }

  // Check if all select values are unique
  const selectUniqueValues = new Set(
    Object.values(selectElements).map((select) => select.value)
  );
  if (selectUniqueValues.size !== selectElements.length) {
    return "All select values must be unique";
  }

  // Check if all input values are unique
  const inputUniqueValues = new Set(
    Object.values(inputElements).map((input) => input.value)
  );
  if (inputUniqueValues.size !== inputElements.length) {
    return "All input values must be unique";
  }

  return null;
}

// Handle form submission and send data to API
async function handleSubmit(event, selectedMode) {
  event.preventDefault();

  const selectPlayersContainer = document.getElementById(
    "select-players-container"
  );
  const selectElements = selectPlayersContainer.querySelectorAll("select");
  const inputElements = selectPlayersContainer.querySelectorAll("input");

  const players = Array.from(selectElements).map((select, index) => {
    return {
      id: select.value,
      name: inputElements[index].value,
    };
  });

  const data = {
    mode: selectedMode,
    players: players,
  };

  const validationResult = validateForm();
  if (validationResult) {
    console.log(validationResult);
    return;
  }

  console.log(data);

  // Send data to API
}

// Create and add the submit button dynamically
function createSubmitButton(container, selectedMode) {
  const div = document.createElement("div");
  div.className = "row";

  const submitButton = document.createElement("button");
  submitButton.type = "submit";
  submitButton.className = "btn btn-light btn-lg mt-4";
  submitButton.textContent = "Submit";
  div.appendChild(submitButton);
  container.appendChild(div);
}

// Create and add multiple player select elements
function createMultipleSelectElements(container, users, count) {
  for (let i = 0; i < count; i++) {
    container.appendChild(createSelectElement(users));
  }
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
      createSubmitButton(selectPlayersContainer, selectedMode);
      break;
    case "tournament":
      createMultipleSelectElements(selectPlayersContainer, users, 4);
      createSubmitButton(selectPlayersContainer, selectedMode);
      break;
    default:
      selectPlayersContainer.innerHTML = "<h1>No mode selected</h1>";
      break;
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
  const form = document.getElementById("game-form");

  btn1v1.addEventListener("click", function () {
    selectedMode = "1v1";
    updateModeSelection(btn1v1, btnTournament, "1v1", users);
  });

  btnTournament.addEventListener("click", function () {
    selectedMode = "tournament";
    updateModeSelection(btnTournament, btn1v1, "tournament", users);
  });

  form.addEventListener("submit", function (event) {
    handleSubmit(event, selectedMode);
  });

  updateSelectPlayersContainer(users, selectedMode);
}
