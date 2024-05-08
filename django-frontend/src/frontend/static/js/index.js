import { fetchChat, handleAddFriendListClick,  handleFriendRequestsListClick, handleFriendListClick } from './sidebar.js';
import { fileInputListener, editNicknameListener, profileExitButtonListener } from './profile.js';
import { toggleProfile } from './topbar.js';

// Fetch and inject sidebar content
window.addEventListener('DOMContentLoaded', () => {
	fetch('/sidebar/')
		.then(response => response.text())
		.then(data => {
			document.querySelector('.sidebar-container').innerHTML = data;

			// fetch chat inside sidebar
			fetchChat();

			// sidebar event handlers
			handleFriendListClick();
			handleFriendRequestsListClick();
			handleAddFriendListClick();
		})
		.catch(error => console.error('Error fetching sidebar:', error));
});

// Fetch and inject topbar content
window.addEventListener('DOMContentLoaded', () => {
	fetch('/topbar/')
		.then(response => response.text())
		.then(data => {
			document.querySelector('.topbar-container').innerHTML = data;

			// topbar event handlers
			toggleProfile();
		})
		.catch(error => console.error('Error fetching topbar:', error));
});

// Fetch and inject profile content
window.addEventListener('DOMContentLoaded', () => {
	fetch('/profile/')
	.then(response => response.text())
	.then(data => {
		document.querySelector('.profile-container').innerHTML = data;

		// profile event handlers
		profileExitButtonListener();
		editNicknameListener();
		fileInputListener();
	})
	.catch(error => console.error('Error fetching profile:', error));
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