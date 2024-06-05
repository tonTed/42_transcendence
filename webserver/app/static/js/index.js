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


const BASE_URL = 'http://localhost:8000/app';

class ContentLoader {
	constructor(baseurl) {
		this.baseurl = baseurl;
	}

	async fromFetch(endpoint, containerId) {
		const response = await fetch(
			`${this.baseurl}/${endpoint}`,
			{
				method: 'GET',
				credentials: 'include',
			}
		);
		document.getElementById(containerId).innerHTML = await response.text();
	}
}

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

window.addEventListener('DOMContentLoaded', async () => {

	// check is cookie token42 exists
	if (getCookie('token42') === null) {
		window.location.href = 'http://localhost/app/login/';
	}


	const frontendLoader = new ContentLoader(BASE_URL);

	await frontendLoader.fromFetch('topbar/', 'topbarContainer');
	await frontendLoader.fromFetch('friend_list/', 'friendContainer');
	await frontendLoader.fromFetch('chat/', 'chatContainer');
	await frontendLoader.fromFetch('pong/', 'gameContainer');
	await frontendLoader.fromFetch('profile/', 'profileContainer');

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