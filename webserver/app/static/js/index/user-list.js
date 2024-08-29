import { updateFriendship } from "../api.js";

function handleToggleFriendship() {
  const buttons = document.querySelectorAll(".toggle-friendship");
  buttons.forEach((button) => {
    button.onclick = async function () {
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

export { handleToggleFriendship };
