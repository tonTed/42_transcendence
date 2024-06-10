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
		history: { endpoint: 'history/', containerId: 'historyContainer' },
		profile: { endpoint: 'profile/', containerId: 'profileContainer' }
	}
};

window.addEventListener('DOMContentLoaded', async () => {

	const jwtToken = getCookie('jwt_token');
	const isValid = await fetch('/api/auth/verify/', {
		method: 'POST',
		headers: {
			Authorization: `${jwtToken}`
		}
	});

	if (isValid.status !== 200) {
		window.location.href = '/login';
	}

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

	// TODO: Refactor in other functions
	const liveUpdateSocket = new WebSocket('ws://localhost:3000/ws/live-update/');
	liveUpdateSocket.onopen = () => {
		console.debug('live-update socket opened');
	};

	liveUpdateSocket.onmessage = (event) => {
		const eventData = JSON.parse(event.data);
		for (const event of eventData.data.split(',')) {
			indexLoader.load(event);
		}
	};

	liveUpdateSocket.onclose = () => {
		console.debug('live-update socket closed');
	};
});

