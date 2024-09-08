import { updateFriendship } from "../api.js";
import { contentLoader } from "./index.js";

function handleToggleFriendship() {
  const buttons = document.querySelectorAll(".toggle-friendship");
  buttons.forEach((button) => {
    button.onclick = async function () {
      button.onclick = ()=> {};
      const user_id = button.getAttribute("data-user-id");
      const friend_status = button.getAttribute("data-friend-status");

      try {
        await updateFriendship(user_id, friend_status);
      } catch (error) {
        alert("Error updating friend status:", error);
      }
    };
  });
}

function handleUserSelection() {
  const buttons = document.querySelectorAll(".user-name");
  buttons.forEach((button) => {
    button.onclick = function () {
      const user_id = button.getAttribute("data-user-id");
      contentLoader.load("history", `user_id=${user_id}`);
    };
  });
}

export { handleToggleFriendship, handleUserSelection };
