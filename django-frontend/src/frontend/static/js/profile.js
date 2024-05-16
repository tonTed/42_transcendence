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
    var editNicknameButton = document.getElementById("editNicknameButton");
    editNicknameButton.addEventListener("click", function() {
        var nicknameInput = document.getElementById("editNicknameInput");
        var confirmNicknameButton = document.getElementById("confirmNicknameButton");
        var nickname = document.getElementById("nickname");
        
        nicknameInput.style.display = "flex";
        nickname.style.display = "none";
        editNicknameButton.style.display = "none"
        confirmNicknameButton.style.display = "flex"
    })
}

function confirmNicknameButtonListener() {
    var confirmUsernameButton = document.getElementById("confirmNicknameButton");
    confirmUsernameButton.addEventListener("click", function() {
        var username = document.getElementById("nickname");
        var usernameInput = document.getElementById("editNicknameInput");
        var newUsername = usernameInput.value;
        
        
        // API call
        (async () => {
            await updateUsername(newUsername);
        })();

        // display
        usernameInput.style.display = "none";
        username.style.display = "flex";
        editNicknameButton.style.display = "flex"
        confirmUsernameButton.style.display = "none"
    })
}

const updateUsername = async (newUsername) => {
    const url = `http://localhost:3000/api/users/${userId}/`;
    const data = {
        username: newUsername,
    };

    try {
        const response = await fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            const updatedUser = await response.json();
            console.log('User updated successfully:', updatedUser);
        } else {
            console.error('Failed to update user:', response.statusText);
        }
    } catch (error) {
        console.error('Error:', error);
    }
};

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