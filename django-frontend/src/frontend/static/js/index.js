import { handleAddFriendListClick,  handleFriendRequestsListClick, handleFriendListClick } from './sidebar.js';
import { fileInputListener, editUsernameButtonListener, confirmUsernameButtonListener, toggle2FA, confirmAvatarButtonListener, profileExitButtonListener } from './profile.js';
import { toggleProfile } from './topbar.js';

window.addEventListener('DOMContentLoaded', () => {
	// sidebar
	handleAddFriendListClick();
	handleFriendRequestsListClick();
	handleFriendListClick();
	
	// profile
	fileInputListener();
	editUsernameButtonListener();
	confirmUsernameButtonListener();
	confirmAvatarButtonListener();
	profileExitButtonListener();
	toggle2FA();
	toggleProfile();
});