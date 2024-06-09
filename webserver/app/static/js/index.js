import { loadCanvasGame } from './pong/main.js';
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

import { ContentLoader } from './ContentLoader.js';


const BASE_URL = 'frontend';

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Vérifier si ce cookie commence par le nom recherché
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const contentLoaderConfig = {
	baseurl: BASE_URL,
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


	const frontendLoader = new ContentLoader(contentLoaderConfig);
	await frontendLoader.loadAll();

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