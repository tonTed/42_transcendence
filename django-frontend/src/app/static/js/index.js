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
	fetch('/game/')
		.then(response => response.text())
		.then(data => {
			document.querySelector('.game-container').innerHTML = data;
		})
		.catch(error => console.error('Error fetching game:', error));
});