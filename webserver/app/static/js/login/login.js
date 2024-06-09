import { ContentLoader } from '../ContentLoader.js';

const loginLoaderConfig = {
	baseurl: 'frontend',
	routes: {
		login: { endpoint: 'login/', containerId: 'loginContainer' },
	}
};


window.addEventListener('DOMContentLoaded', async () => {

	const frontendLoader = new ContentLoader(loginLoaderConfig);

	await frontendLoader.loadAll();
});

