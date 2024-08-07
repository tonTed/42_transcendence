import { getCookie } from "./utils.js";

/**
 * @typedef {import("./types.js").Player} Player
 * @typedef {import("./types.js").Game} Game
 * @typedef {import("./types.js").Tournament} Tournament
 */

const GAME = [
  {
    id: 1,
    player1: {
      id: 1,
      name: "hlander",
    },
    player2: {
      id: 2,
      name: "helene",
    },
    status: "not_started",
    winner: null,
    player1_score: 0,
    player2_score: 0,
  },
];

const GAMES = [
  {
    id: 1,
    player1: {
      id: 1,
      name: "hlander",
    },
    player2: {
      id: 2,
      name: "helene",
    },
    status: "finished",
    winner: 1,
    player1_score: 3,
    player2_score: 2,
  },
  {
    id: 2,
    player1: {
      id: 3,
      name: "naberri",
    },
    player2: {
      id: 4,
      name: "byaqine",
    },
    status: "in_progress",
    winner: null,
    player1_score: 0,
    player2_score: 0,
  },
  {
    id: 3,
    player1: {
      id: 1,
      name: "hlander",
    },
    player2: {
      id: null,
      name: null,
    },
    status: "not_started",
    winner: null,
    player1_score: 0,
    player2_score: 0,
  },
  {
    id: 2,
    player1: {
      id: 2,
      name: "helene",
    },
    player2: {
      id: null,
      name: null,
    },
    status: "not_started",
    winner: null,
    player1_score: 0,
    player2_score: 0,
  },
];

const TOURNAMENTS = {
  id: 1,
  status: "in_progress",
  games: GAMES,
};

const makeApiRequest = async (endpoint, method, data) => {
  const url = `${endpoint}`;
  const csrfToken = getCookie("csrftoken");
  const headers = {
    "X-CSRFToken": csrfToken,
  };

  let formData = null;
  if (method !== "GET") {
    formData = new FormData();
    for (const key in data) {
      formData.append(key, data[key]);
    }
  }

  const fetchOptions = {
    method,
    headers,
    credentials: "include",
    body: formData ? formData : undefined,
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
    console.debug("Username updated successfully:", updatedUser);
    return updatedUser;
  } catch (error) {
    console.error("Failed to update username:", error);
  }
};

const updateAvatar = async (avatar) => {
  try {
    const updatedUser = await makeApiRequest(
      "api/users/updateAvatar/",
      "PATCH",
      { avatar }
    );
    console.debug("Avatar updated successfully:", updatedUser);
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
    console.debug("Friendship updated successfully:", updatedFriendship);
    return updatedFriendship;
  } catch (error) {
    console.error("Error updating friend status:", error);
  }
};

const getUsers = async () => {
  try {
    const users = await makeApiRequest("api/users/", "GET");
    console.debug("Users fetched successfully");
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
  console.log("players", players);
  return GAME;
};

/**
 * @param {Player[]} players - array of players
 *
 * @returns {Tournament} tournament - tournament object
 */
const createTournament = (players) => {
  console.log("players", players);
  return TOURNAMENTS;
};

export {
  updateUsername,
  updateAvatar,
  updateFriendship,
  getUsers,
  createGame,
  createTournament,
};
