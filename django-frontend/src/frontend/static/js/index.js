import { handleAddFriendListClick,  handleFriendRequestsListClick, handleFriendListClick } from './sidebar.js';
import { fileInputListener, editNicknameButtonListener, confirmNicknameButtonListener, profileExitButtonListener } from './profile.js';
import { toggleProfile } from './topbar.js';

window.addEventListener('DOMContentLoaded', () => {
	// sidebar
	handleAddFriendListClick();
	handleFriendRequestsListClick();
	handleFriendListClick();

	// profile
	fileInputListener();
	editNicknameButtonListener();
	confirmNicknameButtonListener();
	profileExitButtonListener();

	// profile
	toggleProfile();
});