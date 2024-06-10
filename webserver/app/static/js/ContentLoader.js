

export class ContentLoader {
	constructor(config) {
		this.baseurl = config.baseurl;
		this.routes = config.routes;
		this.jwt_token = null;
	}

    /**
     * Load the content for a single route
     * @param {string} endpoint - The endpoint to load
     * @example : 
     *  this.load('topbar');
     */
	async load(endpoint) {
		const route = this.routes[endpoint];
		if (route) {
			console.debug(`Loading ${endpoint}`);
			const response = await fetch(
                `${this.baseurl}/${route.endpoint}`,
                {
                    method: 'GET',
                    credentials: 'include',
					headers: {
						'Authorization': `Bearer ${this.jwt_token}`
					}
                }
            );
			document.getElementById(route.containerId).innerHTML = await response.text();
		}
	}
    
    /**
     * Load all the content for all the routes
     */
	async loadAll() {
		for (const endpoint in this.routes) {
			await this.load(endpoint);
		}
	}

	setJwtToken(jwt_token) {
		this.jwt_token = jwt_token;
	}
}
