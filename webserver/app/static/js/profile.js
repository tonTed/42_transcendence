import { updateUsername, updateAvatar } from './edit_profile.js';

function fileInputListener() {
    const fileInput = document.getElementById('imageInput');
    if (fileInput) {
        fileInput.addEventListener('change', function () {
            const fileName = fileInput.files.length > 0 ? fileInput.files[0].name : 'No file chosen';
            const fileNameDisplay = document.getElementById('fileName');
            fileNameDisplay.textContent = fileName;
        });
    } else {
        console.error('File input not found!');
    }
}

function editUsernameButtonListener() {
    const editUsernameButton = document.getElementById("editUsernameButton");
    editUsernameButton.addEventListener("click", function() {
        const usernameInput = document.getElementById("editUsernameInput");
        const confirmUsernameButton = document.getElementById("confirmUsernameButton");
        const username = document.getElementById("username");

        usernameInput.style.display = "flex";
        username.style.display = "none";
        editUsernameButton.style.display = "none"
        confirmUsernameButton.style.display = "flex"
    })
}

function confirmUsernameButtonListener() {
    const confirmUsernameButton = document.getElementById("confirmUsernameButton");
    confirmUsernameButton.addEventListener("click", function() {
        const editUsernameButton = document.getElementById("editUsernameButton");
        const username = document.getElementById("username");
        const topbarUsername = document.getElementById("accountUsername");
        const usernameInput = document.getElementById("editUsernameInput");
        const newUsername = usernameInput.value;
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
    const confirmAvatarButton = document.getElementById("confirmAvatarButton");
    confirmAvatarButton.addEventListener("click", function() {
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
                const newAvatarUrl = await updateAvatar(avatar);
                const updatedUrl = newAvatarUrl.replace('http://api-users:3001', 'http://localhost:3001');

                // change avatar in topbar
                topbar_avatar.src = updatedUrl;
            } catch (error) {
                console.error("Failed to update avatar in topbar:", error);
            }
        })();
        
    })
}

function toggle2FA() {
    const toggleSwitch = document.getElementById('toggle2fa');
    toggleSwitch.addEventListener('change', function(event) {
        const infoType = document.getElementById('activate_deactivate_2fa');
        const password2fa = document.getElementById("password2fa");

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
    const profileExitButton = document.getElementById("profileExitButton");
    profileExitButton.addEventListener("click", function() {
        const gameContainer = document.getElementById("gameContainer");
        const profileContainer = document.getElementById("profileContainer");

        gameContainer.style.display = "flex";
        profileContainer.style.display = "none";
    })
}

export { fileInputListener, editUsernameButtonListener, profileExitButtonListener, confirmUsernameButtonListener, confirmAvatarButtonListener, toggle2FA };