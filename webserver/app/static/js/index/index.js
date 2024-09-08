import { toggleProfile } from "./topbar.js";
import {
  fileInputListener,
  editUsernameButtonListener,
  confirmUsernameButtonListener,
  confirmAvatarButtonListener,
  profileExitButtonListener,
  toggle2FA,
} from "./profile.js";

import { handleToggleFriendship, handleUserSelection } from "./user-list.js";

import { initGameForm } from "./game_form.js";

import { ContentLoader } from "../ContentLoader.js";
import { getCookie } from "../utils.js";
import liveUpdateManager from "./live_update_manager.js";

// import { initializeHistoryTabs } from "./history.js";

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

export const contentLoader = new ContentLoader(contentLoaderConfig);

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
    return;
  }

  contentLoader.setJwtToken(jwtToken);
  await contentLoader.loadAll();

  initializeEventListeners();
  liveUpdateManager(contentLoader, initializeEventListeners);
});

function initializeEventListeners() {
  handleToggleFriendship();
  handleUserSelection();
  fileInputListener();
  editUsernameButtonListener();
  confirmUsernameButtonListener();
  confirmAvatarButtonListener();
  profileExitButtonListener();
  toggle2FA();
  toggleProfile();
  initGameForm();
  // initializeHistoryTabs();
}
