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

function editNicknameListener() {
    var editButton = document.getElementById("editNicknameButton");
    editButton.addEventListener("click", function() {
        var nicknameInput = document.getElementById("editNicknameInput");
        var nicknameButton = document.getElementById("editNicknameButton");
        var nickname = document.getElementById("nickname");

        if (nickname.style.display === "flex") {
            nicknameInput.style.display = "flex";
            nickname.style.display = "none";
            nicknameButton.innerHTML = "Confirm"
        } else {
            nicknameInput.style.display = "none";
            nickname.style.display = "flex";
            nicknameButton.innerHTML = "Edit"
        }
    })
}

export { fileInputListener, editNicknameListener };