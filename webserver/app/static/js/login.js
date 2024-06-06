

const BASE_URL = 'http://localhost/frontend';

export class ContentLoader {
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

	await frontendLoader.fromFetch('login/', 'loginContainer');
});