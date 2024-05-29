const BASE_URL = 'http://localhost:8000/app';


// Example 1
class ContentLoader {
	constructor(baseurl) {
		this.baseurl = baseurl;
	}

	async loadContent(endpoint, containerId) {
		const response = await fetch(`${this.baseurl}/${endpoint}`);
		document.getElementById(containerId).innerHTML = await response.text();
	}

	async topbar() {
		await this.loadContent('topbar/', 'topbarContainer');
	}

	async friendList() {
		await this.loadContent('friend_list/', 'friendContainer');
	}

	async chat() {
		await this.loadContent('chat/', 'chatContainer');
	}

	async pong() {
		await this.loadContent('pong/', 'gameContainer');
	}

	async loadAll() {
		await this.topbar();
		await this.friendList();
		await this.chat();
		await this.pong();
	}
}

window.addEventListener('DOMContentLoaded', async () => {
	const frontendLoader = new ContentLoader(BASE_URL);

	await frontendLoader.loadAll();
	await frontendLoader.topbar();
});

const BASE_URL = 'http://localhost:8000/app';


// Example 2
class ContentLoader2 {
	constructor(baseurl, routes) {
		this.baseurl = baseurl;
		this.routes = routes;
	}

	async load(endpoint) {
		const route = this.routes.find(route => route.endpoint === endpoint);
		if (route) {
			const response = await fetch(`${this.baseurl}/${route.endpoint}`);
			document.getElementById(route.containerId).innerHTML = await response.text();
		}
	}

	async loadAll() {
		for (const route of this.routes) {
			await this.load(route.endpoint);
		}
	}
}

const routes = [
	{ endpoint: 'topbar/', containerId: 'topbarContainer' },
	{ endpoint: 'friend_list/', containerId: 'friendContainer' },
	{ endpoint: 'chat/', containerId: 'chatContainer' },
	{ endpoint: 'pong/', containerId: 'gameContainer' }
];

window.addEventListener('DOMContentLoaded', async () => {
	const frontendLoader = new ContentLoader2(BASE_URL, routes);

	await frontendLoader.loadAll();
	await frontendLoader.load('topbar/');
});

const BASE_URL = 'http://localhost:8000/app';


// Example 3
class ContentLoader3 {
	constructor(config) {
		this.baseurl = config.baseurl;
		this.routes = config.routes;
	}

	async load(endpoint) {
		const route = this.routes[endpoint];
		if (route) {
			const response = await fetch(`${this.baseurl}/${route.endpoint}`);
			document.getElementById(route.containerId).innerHTML = await response.text();
		}
	}

	async loadAll() {
		for (const endpoint in this.routes) {
			await this.load(endpoint);
		}
	}
}

const config = {
	baseurl: BASE_URL,
	routes: {
		topbar: { endpoint: 'topbar/', containerId: 'topbarContainer' },
		friendList: { endpoint: 'friend_list/', containerId: 'friendContainer' },
		chat: { endpoint: 'chat/', containerId: 'chatContainer' },
		pong: { endpoint: 'pong/', containerId: 'gameContainer' }
	}
};

window.addEventListener('DOMContentLoaded', async () => {
	const frontendLoader = new ContentLoader3(config);

	await frontendLoader.loadAll();
	await frontendLoader.load('topbar/');
});

// Example avec LiveUpdateManager
const BASE_URL = 'http://localhost:8000/app';

class ContentLoader4 {
	constructor(baseurl) {
		this.baseurl = baseurl;
		this.routes = {};
	}

	async load(endpoint) {
		const route = this.routes[endpoint];
		if (route) {
			const response = await fetch(`${this.baseurl}/${route.endpoint}`);
			document.getElementById(route.containerId).innerHTML = await response.text();
		}
	}

	async loadAll() {
		for (const endpoint in this.routes) {
			await this.load(endpoint);
		}
	}

	setRoutes(routes) {
		this.routes = routes;
	}
}

class LiveUpdateManager {
	constructor(contentLoader, wsUrl) {
		this.contentLoader = contentLoader;
		this.ws = new WebSocket(wsUrl);
		this.ws.onmessage = (event) => this.handleMessage(event);
	}

	handleMessage(event) {
		const message = JSON.parse(event.data);
		if (message.route) {
			this.contentLoader.load(message.route);
		}
	}
}

const routes = {
	topbar: { endpoint: 'topbar/', containerId: 'topbarContainer' },
	friendList: { endpoint: 'friend_list/', containerId: 'friendContainer' },
	chat: { endpoint: 'chat/', containerId: 'chatContainer' },
	pong: { endpoint: 'pong/', containerId: 'gameContainer' }
};

window.addEventListener('DOMContentLoaded', async () => {
	const contentLoader = new ContentLoader(BASE_URL);
	contentLoader.setRoutes(routes);

	const liveUpdateManager = new LiveUpdateManager(contentLoader, 'ws://localhost:8000/ws');

	await contentLoader.loadAll();
	await contentLoader.load('topbar/');
});


