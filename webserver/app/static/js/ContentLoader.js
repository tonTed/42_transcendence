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
  async load(endpoint, params = "") {
    const route = this.routes[endpoint];
    if (route) {
      console.debug(`Loading ${endpoint}`);
      const response = await fetch(
        `${this.baseurl}/${route.endpoint}?${params}`,
        {
          method: "GET",
          credentials: "include",
          headers: {
            Authorization: `${this.jwt_token}`,
          },
        }
      );
      if (response.status === 401) {
        alert("You are not authorized to access this page");
        window.location.href = "/login";
      }
      document.getElementById(route.containerId).innerHTML =
        await response.text();
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
