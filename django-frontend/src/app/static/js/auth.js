// change to login form
function showLoginForm() {
	document.getElementById('loginForm').style.display = '';
	document.getElementById('registerForm').style.display = 'none';
}

// change to register form
function showRegisterForm() {
	document.getElementById('loginForm').style.display = 'none';
	document.getElementById('registerForm').style.display = '';
}

// dislpay avatar file name
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('avatarInput').addEventListener('change', function() {
        var fileName = 'No file chosen';
        if (this.files && this.files.length > 0) {
            fileName = this.files[0].name;
        }
        document.getElementById('fileName').textContent = fileName;
    });
});