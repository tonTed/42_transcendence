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
    var confirmNicknameButton = document.getElementById("confirmNicknameButton");
    confirmNicknameButton.addEventListener("click", function() {
        var nickname = document.getElementById("nickname");
        var nicknameInput = document.getElementById("editNicknameInput");
        
        nicknameInput.style.display = "none";
        nickname.style.display = "flex";
        editNicknameButton.style.display = "flex"
        confirmNicknameButton.style.display = "none"

        // API call
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