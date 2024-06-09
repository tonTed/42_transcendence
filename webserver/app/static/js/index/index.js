import { loadCanvasGame } from '../pong/main.js';
import { toggleProfile } from './topbar.js';
import {
	handleAddFriendListClick,
	handleFriendRequestsListClick,
	handleFriendListClick,
} from './sidebar.js';
import {
	fileInputListener,
	editUsernameButtonListener,
	confirmUsernameButtonListener,
	confirmAvatarButtonListener,
	profileExitButtonListener,
	toggle2FA,
} from './profile.js';

import { ContentLoader } from '../ContentLoader.js';
import { getCookie } from '../utils.js';

const contentLoaderConfig = {
	baseurl: 'frontend',
	routes: {
		topbar: { endpoint: 'topbar/', containerId: 'topbarContainer' },
		friendList: { endpoint: 'friend_list/', containerId: 'friendContainer' },
		chat: { endpoint: 'chat/', containerId: 'chatContainer' },
		pong: { endpoint: 'pong/', containerId: 'gameContainer' },
		profile: { endpoint: 'profile/', containerId: 'profileContainer' }
	}
};

window.addEventListener('DOMContentLoaded', async () => {

	// check is cookie token42 exists
	if (getCookie('token42') === null) {
		window.location.href = '/login';
	}

	const liveUpdateSocket = new WebSocket('ws://localhost:3000/ws/live-update/');
	liveUpdateSocket.onopen = () => {
		console.log('WebSocket connection opened');
	};
	liveUpdateSocket.onclose = () => {
		console.log('WebSocket connection closed');
	};


	const indexLoader = new ContentLoader(contentLoaderConfig);
	await indexLoader.loadAll();

	await loadCanvasGame();

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