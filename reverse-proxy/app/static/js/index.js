import { loadCanvasGame } from './pong/main.js';


const BASE_URL = 'http://localhost:8000/app';

class ContentLoader {
	constructor(baseurl) {
		this.baseurl = baseurl;
	}

	async fromFetch(endpoint, containerId) {
		const response = await fetch(`${this.baseurl}/${endpoint}`);
		document.getElementById(containerId).innerHTML = await response.text();
	}
}

window.addEventListener('DOMContentLoaded', async () => {

	const frontendLoader = new ContentLoader(BASE_URL);

	await frontendLoader.fromFetch('topbar/', 'topbarContainer');
	await frontendLoader.fromFetch('friend_list/', 'friendContainer');
	await frontendLoader.fromFetch('chat/', 'chatContainer');
	await frontendLoader.fromFetch('pong/', 'gameContainer');

	await loadCanvasGame();
});