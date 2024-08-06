import { loadCanvasGame } from "../pong/main.js";
import { toggleProfile } from "./topbar.js";
import {
  fileInputListener,
  editUsernameButtonListener,
  confirmUsernameButtonListener,
  confirmAvatarButtonListener,
  profileExitButtonListener,
  toggle2FA,
} from "./profile.js";

import { handleToggleFriendship } from "./user-list.js";

import { initGameForm } from "./game_form.js";

import { ContentLoader } from "../ContentLoader.js";
import { getCookie } from "../utils.js";

const contentLoaderConfig = {
  baseurl: "frontend",
  routes: {
    topbar: { endpoint: "topbar/", containerId: "topbarContainer" },
    users_list: { endpoint: "users_list/", containerId: "userContainer" },
    history: { endpoint: "history/", containerId: "historyContainer" },
    profile: { endpoint: "profile/", containerId: "profileContainer" },
    form_game: { endpoint: "form_game/", containerId: "gameContainer" },
  },
};

window.addEventListener("DOMContentLoaded", async () => {
  const jwtToken = getCookie("jwt_token");
  const isValid = await fetch("/api/auth/verify/", {
    method: "POST",
    headers: {
      Authorization: `${jwtToken}`,
    },
  });

  if (isValid.status !== 200) {
    window.location.href = "/login";
  }

  const indexLoader = new ContentLoader(contentLoaderConfig);
  indexLoader.setJwtToken(jwtToken);
  await indexLoader.loadAll();

  await loadCanvasGame();

  initializeEventListeners();

  // TODO: Refactor in other functions
  const liveUpdateSocket = new WebSocket("ws://localhost:3000/ws/live-update/");
  liveUpdateSocket.onopen = () => {
    console.debug("live-update socket opened");
  };

  liveUpdateSocket.onmessage = async (event) => {
    const eventData = JSON.parse(event.data);
    for (const event of eventData.data.split(",")) {
      await indexLoader.load(event);
    }
    initializeEventListeners();
  };

  liveUpdateSocket.onclose = () => {
    console.debug("live-update socket closed");
  };
});

function initializeEventListeners() {
  handleToggleFriendship();
  fileInputListener();
  editUsernameButtonListener();
  confirmUsernameButtonListener();
  confirmAvatarButtonListener();
  profileExitButtonListener();
  toggle2FA();
  toggleProfile();
  initGameForm();
}
