function displayGames(games) {
  console.log("displayGames");
  const container = document.getElementById("gameContainer");
  container.innerHTML = "";

  const table = document.createElement("table");
  table.classList.add("table");
  table.style.width = "75%";
  table.style.border = "1px solid #000";
  table.style.margin = "0 auto";

  const thead = document.createElement("thead");
  const tbody = document.createElement("tbody");

  thead.innerHTML =
    "<tr class='table-dark'><th scope='col'>Game</th><th scope='col'>Status</th><th class='text-center' scope='col'>Player</th><th class='text-center' scope='col'>Player</th></tr>";

  games.forEach((game, index) => {
    let colorByStatus = "";
    switch (game.status) {
      case "not_started":
        colorByStatus = "badge text-bg-warning";
        break;
      case "in_progress":
        colorByStatus = "badge text-bg-info";
        break;
      case "finished":
        colorByStatus = "badge text-bg-success";
        break;
    }
    const gameItem = document.createElement("tr");
    const player1 = game.player1.name ? game.player1.name : "TBD";
    const player2 = game.player2.name ? game.player2.name : "TBD";
    gameItem.innerHTML = `
      <th scope='row'>${index + 1}</th>
      <td><span class='${colorByStatus}'>${game.status}</span></td>
      <td class='text-center ${
        game.winner && game.winner === game.player1.id ? "text-bg-success" : ""
      }'>${player1}</td>
      <td class='text-center ${
        game.winner && game.winner === game.player2.id ? "text-bg-success" : ""
      }'>${player2}</td>
    `;
    tbody.appendChild(gameItem);
  });

  table.appendChild(thead);
  table.appendChild(tbody);
  container.appendChild(table);
}

export { displayGames };
