import { updateUsername, updateAvatar } from './edit_profile.js';

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

function editUsernameButtonListener() {
    var editUsernameButton = document.getElementById("editUsernameButton");
    editUsernameButton.addEventListener("click", function() {
        var usernameInput = document.getElementById("editUsernameInput");
        var confirmUsernameButton = document.getElementById("confirmUsernameButton");
        var username = document.getElementById("username");

        usernameInput.style.display = "flex";
        username.style.display = "none";
        editUsernameButton.style.display = "none"
        confirmUsernameButton.style.display = "flex"
    })
}

function confirmUsernameButtonListener() {
    var confirmUsernameButton = document.getElementById("confirmUsernameButton");
    confirmUsernameButton.addEventListener("click", function() {
        var editUsernameButton = document.getElementById("editUsernameButton");
        var username = document.getElementById("username");
        var topbarUsername = document.getElementById("accountUsername");
        var usernameInput = document.getElementById("editUsernameInput");
        var newUsername = usernameInput.value;
        if (newUsername.length === 0) {
            alert("Please choose a username first.");
            return ;
        }

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

function confirmAvatarButtonListener() {
    var confirmAvatarButton = document.getElementById("confirmAvatarButton");
    confirmAvatarButton.addEventListener("click", function() {
        var imageInput = document.getElementById("imageInput");
        var topbar_avatar = document.getElementById("");
        if (imageInput.files.length === 0) {
            alert("Please choose a file first.");
            return;
        }
        
        
        // API call
        var avatar = imageInput.files[0];

        (async () => {
            await updateAvatar(avatar);
        })();

        // display new avatar on topbar

    })
}

function toggle2FA() {
    var toggleSwitch = document.getElementById('toggle2fa');
    toggleSwitch.addEventListener('change', function(event) {
        var infoType = document.getElementById('activate_deactivate_2fa');
        var password2fa = document.getElementById("password2fa");

        if (event.target.checked) {
            infoType.innerText = "deactivate 2fa";
            password2fa.style.display = "flex";
        } else {
            password2fa.style.display = "none";
            infoType.innerText = "activate 2fa";
        }
    });
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

export { fileInputListener, editUsernameButtonListener, profileExitButtonListener, confirmUsernameButtonListener, confirmAvatarButtonListener, toggle2FA };