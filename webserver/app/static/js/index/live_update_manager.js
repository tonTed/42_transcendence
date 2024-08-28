function liveUpdateManager(contentLoader, initializeEventListeners) {
  const ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
  const ws_path = `${ws_scheme}://${window.location.hostname}/ws/live-update/`;

  const liveUpdateSocket = new WebSocket(ws_path);
  liveUpdateSocket.onopen = () => {
    console.debug("live-update socket opened");
  };

  liveUpdateSocket.onmessage = async (event) => {
    const eventData = JSON.parse(event.data);
    for (const event of eventData.data.split(",")) {
      await contentLoader.load(event);
    }
    initializeEventListeners();
  };

  liveUpdateSocket.onclose = () => {
    console.debug("live-update socket closed");
  };
}

export default liveUpdateManager;
