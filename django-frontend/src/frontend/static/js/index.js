import { handleAddFriendListClick,  handleFriendRequestsListClick, handleFriendListClick } from './sidebar.js';
import { fileInputListener, editUsernameButtonListener, confirmUsernameButtonListener, profileExitButtonListener } from './profile.js';
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
	profileExitButtonListener();
	
	// profile
	toggleProfile();
});