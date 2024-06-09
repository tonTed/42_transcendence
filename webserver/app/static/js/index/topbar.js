function toggleProfile() {
    const accountInfos = document.getElementById("accountInfos");
    accountInfos.addEventListener("click", function() {
      const gameContainer = document.getElementById("gameContainer");
      const profileContainer = document.getElementById("profileContainer");

      if (profileContainer.style.display !== "flex") {
        gameContainer.style.display = "none";
        profileContainer.style.display = "flex";
      }
    })
}

export { toggleProfile }