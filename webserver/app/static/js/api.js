import { getCookie } from "./utils.js";

/**
 * @typedef {import("./types.js").Player} Player
 * @typedef {import("./types.js").Game} Game
 * @typedef {import("./types.js").Tournament} Tournament
 */

const makeApiRequest = async (endpoint, method, data) => {
  const url = `${endpoint}`;
  const csrfToken = getCookie("csrftoken");
  const jwtToken = getCookie("jwt_token");
  const headers = {
    "X-CSRFToken": csrfToken,
    "Content-Type": "application/json",
    Authorization: jwtToken,
  };

  const fetchOptions = {
    method,
    headers,
    credentials: "include",
    body: data ? JSON.stringify(data) : undefined,
  };

  const response = await fetch(url, fetchOptions);
  if (!response.ok) {
    throw new Error(response.statusText);
  }
  return await response.json();
};

const updateUsername = async (newUsername) => {
  try {
    const updatedUser = await makeApiRequest(
      "api/users/updateUsername/",
      "PATCH",
      { username: newUsername }
    );
    console.debug("Username updated successfully:", updatedUser.username);
    return updatedUser;
  } catch (error) {
    console.error("Failed to update username:", error);
  }
};

// TODO-TB: try to use makeApiRequest instead of fetch
const updateAvatar = async (avatar) => {
  const formData = new FormData();
  formData.append("avatar", avatar);

  try {
    const response = await fetch("api/users/updateAvatar/", {
      method: "PATCH",
      body: formData,
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
        Authorization: getCookie("jwt_token"),
      },
    });
    const updatedUser = await response.json();
    console.debug("Avatar updated successfully:", updatedUser.username);
    return updatedUser.avatar;
  } catch (error) {
    console.error("Failed to update avatar:", error);
    return null;
  }
};

const updateFriendship = async (user_id, friend_status) => {
  try {
    const updatedFriendship = await makeApiRequest(
      "api/users/update_friend_status/",
      "PATCH",
      {
        friend_id: user_id,
        action: friend_status,
      }
    );
    console.debug("Friendship updated successfully:");
    return updatedFriendship;
  } catch (error) {
    console.error("Error updating friend status:", error);
  }
};

const getUsers = async () => {
  try {
    const users = await makeApiRequest("api/users/", "GET");
    console.debug(`Users fetched successfully (${users.length} users)`);
    return users;
  } catch (error) {
    console.error("Failed to fetch users:", error);
  }
};

/**
 * @param {Player[]} players - array of players
 *
 * @returns {Game[]} games - array of game objects
 */
const createGame = async (players) => {
  return await makeApiRequest("api/games/", "POST", { players });
};

/**
 * @param {Player[]} players - array of players
 *
 * @returns {Tournament} tournament - tournament object
 */
const createTournament = async (players) => {
  return await makeApiRequest("api/games/tournaments/", "POST", { players });
};

const getGamesFromGamesIds = async (games_ids) => {
  const games = [];
  for (const game_id of games_ids) {
    const game = await makeApiRequest(`api/games/${game_id}/`, "GET");
    games.push(game);
  }

  return games;
};

const activate2fa = async () => {
  return await makeApiRequest("api/users/activate_2fa/", "POST");
};

const deactivate2fa = async () => {
  return await makeApiRequest("api/users/deactivate_2fa/", "POST");
};

export {
  updateUsername,
  updateAvatar,
  updateFriendship,
  getUsers,
  createGame,
  createTournament,
  getGamesFromGamesIds,
  activate2fa,
  deactivate2fa,
};
