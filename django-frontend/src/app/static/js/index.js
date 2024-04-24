// Fetch and inject sidebar content
window.addEventListener('DOMContentLoaded', () => {
	fetch('/topbar/')
		.then(response => response.text())
		.then(data => {
			document.querySelector('.topbar-container').innerHTML = data;
		})
		.catch(error => console.error('Error fetching topbar:', error));
});

// Fetch and inject sidebar content
window.addEventListener('DOMContentLoaded', () => {
	fetch('/sidebar/')
		.then(response => response.text())
		.then(data => {
			document.querySelector('.sidebar-container').innerHTML = data;
		})
		.catch(error => console.error('Error fetching sidebar:', error));
});

// Fetch and inject game content
window.addEventListener('DOMContentLoaded', () => {
	fetch('/profile/')
		.then(response => response.text())
		.then(data => {
			document.querySelector('.content-container').innerHTML = data;
		})
		.catch(error => console.error('Error fetching profile:', error));
});