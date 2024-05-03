import { handleAddFriendListClick,  handleFriendRequestsListClick, handleFriendListClick } from './sidebar.js';

// Fetch and inject sidebar content
window.addEventListener('DOMContentLoaded', () => {
	fetch('/sidebar/')
		.then(response => response.text())
		.then(data => {
			document.querySelector('.sidebar-container').innerHTML = data;

			// sidebar event handlers
			handleFriendListClick();
			handleFriendRequestsListClick();
			handleAddFriendListClick();
		})
		.catch(error => console.error('Error fetching sidebar:', error));
});

// Fetch and inject chat
window.addEventListener('DOMContentLoaded', () => {
	fetch('/chat/')
		.then(response => response.text())
		.then(data => {
			document.querySelector('.chat-container').innerHTML = data;
		})
		.catch(error => console.error('Error fetching chat', error));
});

// Fetch and inject topbar content
window.addEventListener('DOMContentLoaded', () => {
	fetch('/topbar/')
		.then(response => response.text())
		.then(data => {
			document.querySelector('.topbar-container').innerHTML = data;
		})
		.catch(error => console.error('Error fetching topbar:', error));
});

// Fetch and inject profile content
window.addEventListener('DOMContentLoaded', () => {
	fetch('/profile/')
	.then(response => response.text())
	.then(data => {
		document.querySelector('.game-profile-container').innerHTML = data;
	})
	.catch(error => console.error('Error fetching profile:', error));
});