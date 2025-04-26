document.addEventListener("DOMContentLoaded", function () {
    const teamsContainer = document.getElementById("teamsContainer");
    const playersContainer = document.getElementById("playersContainer");

    // ✅ Load teams if we are on "teams.html"
    if (teamsContainer) {
        fetchTeams();
    }

    // ✅ Load players if we are on "team_players_2025.html"
    if (playersContainer) {
        const urlParams = new URLSearchParams(window.location.search);
        const teamId = urlParams.get("team_id");
        if (teamId) {
            fetchPlayers(teamId);
        } else {
            playersContainer.innerHTML = "<p>Team ID missing!</p>";
        }
    }
});

// ✅ Fetch Teams
function fetchTeams() {
    fetch("http://127.0.0.1:5000/teams")  
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById("teamsContainer");
            container.innerHTML = "";  

            if (data.length === 0) {
                container.innerHTML = "<p>No teams found.</p>";
                return;
            }

            data.forEach(team => {
                const teamCard = document.createElement("div");
                teamCard.classList.add("team-card");

                let formattedName = team.team_name.replace(/\s+/g, "_");
                let logoPath = `logos/${formattedName}.jpeg`;

                const logo = document.createElement("img");
                logo.src = logoPath;
                logo.classList.add("team-logo");
                logo.onerror = function () {  
                    this.src = "logos/default_logo.jpeg";  
                };

                const name = document.createElement("p");
                name.textContent = team.team_name;
                name.classList.add("team-name");

                // ✅ Clicking a team navigates to the players page
                teamCard.addEventListener("click", function () {
                    window.location.href = `team_players_2025.html?team_id=${team.team_id}`;
                });

                teamCard.appendChild(logo);
                teamCard.appendChild(name);
                container.appendChild(teamCard);
            });
        })
        .catch(error => console.error("Error fetching teams:", error));
}

function fetchPlayers(teamId) {
    fetch(`http://127.0.0.1:5000/players?team_id=${teamId}`)
        .then(response => response.json())
        .then(players => {
            const playersContainer = document.getElementById("playersContainer");
            playersContainer.classList.add("players-container"); // Add grid layout
            playersContainer.innerHTML = "";

            if (players.length === 0) {
                playersContainer.innerHTML = "<p>No players found for this team.</p>";
                return;
            }
            players.forEach(player => {
                const playerCard = document.createElement("div");
                playerCard.classList.add("player-card");
            
                playerCard.innerHTML = `
                    <h3 class="player-name">${player.name}</h3>
                    <p class="player-role"><strong>Role:</strong> ${player.role}</p>
                    <p class="player-price"><strong>Price:</strong> ₹${player.current_price} Cr</p>
                `;
            
                playersContainer.appendChild(playerCard);
            });
        })
        .catch(error => console.error("Error fetching players:", error));
}

// ✅ Player Search Function
function searchPlayers() {
    let query = document.getElementById("playerSearchInput").value;

    if (query.length < 2) {
        document.getElementById("suggestionsList").innerHTML = "";
        return;
    }

    fetch(`http://127.0.0.1:5000/players?search=${query}`)
        .then(response => response.json())
        .then(data => {
            const suggestionsList = document.getElementById("suggestionsList");
            suggestionsList.innerHTML = "";

            if (data.length === 0) {
                suggestionsList.innerHTML = "<li>No players found</li>";
                return;
            }

            data.forEach(player => {
                let listItem = document.createElement("li");
                listItem.textContent = player.name;
                listItem.onclick = function () {
                    fetchPlayerDetails(player.name);
                };
                suggestionsList.appendChild(listItem);
            });
        })
        .catch(error => console.error("Error fetching player data:", error));
}

// ✅ Fetch Individual Player Details
function fetchPlayerDetails(playerName) {
    fetch(`http://127.0.0.1:5000/players?search=${playerName}`)
        .then(response => response.json())
        .then(data => {
            if (data.length === 0) {
                document.getElementById("playerDetails").innerHTML = "<p>Player not found.</p>";
                return;
            }

            let player = data[0];
            document.getElementById("playerDetails").innerHTML = `
                <h3>${player.name}</h3>
                <p>Role: ${player.role}</p>
                <p>Price: ₹${player.current_price} Cr</p>
            `;
        })
        .catch(error => console.error("Error fetching player details:", error));
}
