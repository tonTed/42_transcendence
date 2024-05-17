import { updateUsername } from './edit_profile.js';

function fileInputListener() {
    var fileInput = document.getElementById('imageInput');
    if (fileInput) {
        fileInput.addEventListener('change', function () {
            var fileName = fileInput.files.length > 0 ? fileInput.files[0].name : 'No file chosen';
            var fileNameDisplay = document.getElementById('fileName');
            fileNameDisplay.textContent = fileName;
        });
    } else {
        console.error('File input not found!');
    }
}

function editNicknameButtonListener() {
    var editUsernameButton = document.getElementById("editNicknameButton");
    editUsernameButton.addEventListener("click", function() {
        var usernameInput = document.getElementById("editNicknameInput");
        var confirmUsernameButton = document.getElementById("confirmNicknameButton");
        var username = document.getElementById("nickname");

        usernameInput.style.display = "flex";
        username.style.display = "none";
        editUsernameButton.style.display = "none"
        confirmUsernameButton.style.display = "flex"
    })
}

function confirmNicknameButtonListener() {
    var confirmUsernameButton = document.getElementById("confirmNicknameButton");
    confirmUsernameButton.addEventListener("click", function() {
        var editUsernameButton = document.getElementById("editNicknameButton");
        var username = document.getElementById("nickname");
        var topbarUsername = document.getElementById("accountUsername");
        var usernameInput = document.getElementById("editNicknameInput");
        var newUsername = usernameInput.value;

        // API call
        (async () => {
            await updateUsername(newUsername);
        })();

        // display
        usernameInput.style.display = "none";
        username.style.display = "flex";
        username.innerHTML = newUsername;
        topbarUsername.innerHTML = newUsername;
        editUsernameButton.style.display = "flex"
        confirmUsernameButton.style.display = "none"
    })
}

function profileExitButtonListener() {
    var profileExitButton = document.getElementById("profileExitButton");
    profileExitButton.addEventListener("click", function() {
        var gameContainer = document.getElementById("gameContainer");
        var profileContainer = document.getElementById("profileContainer");

        gameContainer.style.display = "flex";
        profileContainer.style.display = "none";
    })
}

export { fileInputListener, editNicknameButtonListener, profileExitButtonListener, confirmNicknameButtonListener };