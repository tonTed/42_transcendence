import { ContentLoader } from '../ContentLoader.js';

const loginLoaderConfig = {
	baseurl: '/frontend',
	routes: {
		login: { endpoint: 'login/', containerId: 'loginContainer' },
	}
};


window.addEventListener('DOMContentLoaded', async () => {

	const loginLoader = new ContentLoader(loginLoaderConfig);

	await loginLoader.loadAll();
});

