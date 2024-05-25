function toggleProfile() {
    var accountInfos = document.getElementById("accountInfos");
    accountInfos.addEventListener("click", function() {
      var gameContainer = document.getElementById("gameContainer");
      var profileContainer = document.getElementById("profileContainer");

      if (profileContainer.style.display !== "flex") {
        gameContainer.style.display = "none";
        profileContainer.style.display = "flex";
      }
    })
}

export { toggleProfile }