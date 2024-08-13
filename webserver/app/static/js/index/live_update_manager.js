function liveUpdateManager(contentLoader, initializeEventListeners) {
  const liveUpdateSocket = new WebSocket("ws://localhost:3000/ws/live-update/");
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
