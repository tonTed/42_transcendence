import { loadCanvasGame } from '../pong/main.js';
import { toggleProfile } from './topbar.js';
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
		users_list: { endpoint: 'users_list/', containerId: 'userContainer' },
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
	indexLoader.setJwtToken(jwtToken);
	await indexLoader.loadAll();

	await loadCanvasGame();

	initializeEventListeners();

	// TODO: Refactor in other functions
	const liveUpdateSocket = new WebSocket('ws://localhost:3000/ws/live-update/');
	liveUpdateSocket.onopen = () => {
		console.debug('live-update socket opened');
	};

	liveUpdateSocket.onmessage = async (event) => {
		const eventData = JSON.parse(event.data);
		for (const event of eventData.data.split(',')) {
			await indexLoader.load(event);
		}
		initializeEventListeners();	
	};

	liveUpdateSocket.onclose = () => {
		console.debug('live-update socket closed');
	};
});


// TODO: Refactor in other file
const updateFriendship = async (user_id, friend_status) => {
	try {
		const response = await fetch(`/api/users/update_friend_status/`, {
			method: 'PATCH',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': getCookie('csrftoken')
			},
			credentials: 'include',
			body: JSON.stringify({
				friend_id: user_id,
				action: friend_status
			})
		});

		if (!response.ok) {
			const errorData = await response.json();
			throw new Error(errorData.message || 'Unknown error occurred');
		}
	} catch (error) {
		console.error('Error updating friend status:', error);
	}
};

function handleToggleFriendship() {
	const buttons = document.querySelectorAll('.toggle-friendship');
    buttons.forEach(button => {
		button.onclick = async function() {
			const user_id = button.getAttribute('data-user-id');
			const friend_status = button.getAttribute('data-friend-status');

			try {
				await updateFriendship(user_id, friend_status);
			} catch (error) {
				console.error('Error updating friend status:', error);
			}
		};
	});
}

function initializeEventListeners() {
	handleToggleFriendship();
    fileInputListener();
    editUsernameButtonListener();
    confirmUsernameButtonListener();
    confirmAvatarButtonListener();
    profileExitButtonListener();
    toggle2FA();
    toggleProfile();
}
