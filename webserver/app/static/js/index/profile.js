import {
  updateUsername,
  updateAvatar,
  activate2fa,
  deactivate2fa,
} from "../api.js";

function fileInputListener() {
  const fileInput = document.getElementById("imageInput");
  if (fileInput) {
    fileInput.addEventListener("change", function () {
      const fileName =
        fileInput.files.length > 0 ? fileInput.files[0].name : "No file chosen";
      const fileNameDisplay = document.getElementById("fileName");
      fileNameDisplay.textContent = fileName;
    });
  } else {
    console.error("File input not found!");
  }
}

function editUsernameButtonListener() {
  const editUsernameButton = document.getElementById("editUsernameButton");
  editUsernameButton.addEventListener("click", function () {
    const usernameInput = document.getElementById("editUsernameInput");
    const confirmUsernameButton = document.getElementById(
      "confirmUsernameButton"
    );
    const username = document.getElementById("username");

    usernameInput.style.display = "flex";
    username.style.display = "none";
    editUsernameButton.style.display = "none";
    confirmUsernameButton.style.display = "flex";
  });
}

function confirmUsernameButtonListener() {
  const confirmUsernameButton = document.getElementById(
    "confirmUsernameButton"
  );
  confirmUsernameButton.addEventListener("click", function () {
    const editUsernameButton = document.getElementById("editUsernameButton");
    const username = document.getElementById("username");
    const usernameInput = document.getElementById("editUsernameInput");
    const newUsername = usernameInput.value;
    if (newUsername.length === 0) {
      alert("Please choose a username first.");
      return;
    }

    // API call
    (async () => {
      await updateUsername(newUsername);
    })();

    // display
    usernameInput.style.display = "none";
    username.style.display = "flex";
    editUsernameButton.style.display = "flex";
    confirmUsernameButton.style.display = "none";
  });
}

function confirmAvatarButtonListener() {
  const confirmAvatarButton = document.getElementById("confirmAvatarButton");
  confirmAvatarButton.addEventListener("click", function () {
    const imageInput = document.getElementById("imageInput");
    const topbar_avatar = document.getElementById("accountAvatar");

    if (imageInput.files.length === 0) {
      alert("Please choose a file first.");
      return;
    }

    // API call
    const avatar = imageInput.files[0];

    (async () => {
      try {
        await updateAvatar(avatar);
      } catch (error) {
        console.error("Failed to update avatar in topbar:", error);
      }
    })();
  });
}

function toggle2FA() {
  const toggleSwitch = document.getElementById("toggle2fa");
  toggleSwitch.addEventListener("change", function (event) {
    if (event.target.checked) {
      activate2fa();
    } else {
      deactivate2fa();
    }
  });
}

function profileExitButtonListener() {
  const profileExitButton = document.getElementById("profileExitButton");
  profileExitButton.addEventListener("click", function () {
    const gameContainer = document.getElementById("gameContainer");
    const profileContainer = document.getElementById("profileContainer");

    gameContainer.style.display = "flex";
    profileContainer.style.display = "none";
  });
}

export {
  fileInputListener,
  editUsernameButtonListener,
  profileExitButtonListener,
  confirmUsernameButtonListener,
  confirmAvatarButtonListener,
  toggle2FA,
};
