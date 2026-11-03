const players = {
    101: {
        name: "Josh Allen",
        position: "QB"
    },

    102: {
        name: "Lamar Jackson",
        position: "QB"
    },

    103: {
        name: "Justin Jefferson",
        position: "WR"
    },

    104: {
        name: "Saquon Barkley",
        position: "RB"
    },

    105: {
        name: "Travis Kelce",
        position: "TE"
    }
};


let currentTeam = 1;
let currentPick = 1;
let round = 1;

let draftedPlayers = [];

let timeRemaining = 90;
let timerRunning = true;


const draftButton =
    document.getElementById("draftButton");

const playerInput =
    document.getElementById("playerID");

const message =
    document.getElementById("message");

const availableCount =
    document.getElementById("availableCount");

const currentTeamDisplay =
    document.getElementById("currentTeam");

const currentPickDisplay =
    document.getElementById("currentPick");

const pickTeam =
    document.getElementById("pickTeam");

const pickInfo =
    document.getElementById("pickInfo");

const roundNumber =
    document.getElementById("roundNumber");

const progressBar =
    document.getElementById("progressBar");

const progressText =
    document.getElementById("progressText");


draftButton.addEventListener(
    "click",
    draftPlayer
);


function draftPlayer() {

    const selectedID =
        Number(playerInput.value);


    if (!players[selectedID]) {

        message.textContent =
            "Player ID does not exist.";

        return;
    }


    if (draftedPlayers.includes(selectedID)) {

        message.textContent =
            "That player has already been drafted.";

        return;
    }


    const selectedPlayer =
        players[selectedID];


    draftedPlayers.push(selectedID);


    message.textContent =
        "Player Revealed: "
        + selectedPlayer.name
        + " — "
        + selectedPlayer.position;


    addToRoster(
        currentTeam,
        selectedPlayer
    );


    removePlayerRow(selectedID);


    moveToNextPick();


    playerInput.value = "";
}


function addToRoster(team, player) {

    const roster =
        document.getElementById(
            "team" + team + "Roster"
        );


    if (
        roster.textContent.includes(
            "No players drafted"
        )
    ) {

        roster.textContent = "";
    }


    const playerLine =
        document.createElement("div");


    playerLine.textContent =
        player.name
        + " — "
        + player.position;


    roster.appendChild(playerLine);
}


function removePlayerRow(playerID) {

    const row =
        document.querySelector(
            'tr[data-id="'
            + playerID
            + '"]'
        );


    if (row) {
        row.remove();
    }


    availableCount.textContent =
        Object.keys(players).length
        - draftedPlayers.length;
}


function moveToNextPick() {

    currentPick++;


    currentTeam++;


    if (currentTeam > 3) {

        currentTeam = 1;

        round++;
    }


    currentTeamDisplay.textContent =
        "Team " + currentTeam;


    currentPickDisplay.textContent =
        "#" + currentPick;


    pickTeam.textContent =
        "Team " + currentTeam;


    pickInfo.textContent =
        "Round "
        + round
        + " • Pick #"
        + currentPick;


    roundNumber.textContent =
        round;


    updateProgress();


    resetTimer();
}


function updateProgress() {

    const completed =
        draftedPlayers.length;


    const total = 30;


    progressText.textContent =
        completed
        + " / "
        + total
        + " Picks";


    const percentage =
        (completed / total) * 100;


    progressBar.style.width =
        percentage + "%";
}


/* TIMER */

const timerDisplay =
    document.getElementById("timer");

const pauseButton =
    document.getElementById("pauseButton");

const resetButton =
    document.getElementById("resetButton");


setInterval(function () {

    if (
        timerRunning
        &&
        timeRemaining > 0
    ) {

        timeRemaining--;

        updateTimerDisplay();
    }

}, 1000);


function updateTimerDisplay() {

    const minutes =
        Math.floor(
            timeRemaining / 60
        );


    const seconds =
        timeRemaining % 60;


    timerDisplay.textContent =
        String(minutes).padStart(2, "0")
        + ":"
        + String(seconds).padStart(2, "0");
}


pauseButton.addEventListener(
    "click",
    function () {

        timerRunning =
            !timerRunning;


        if (timerRunning) {

            pauseButton.textContent =
                "Pause Timer";

        } else {

            pauseButton.textContent =
                "Resume Timer";
        }

    }
);


resetButton.addEventListener(
    "click",
    resetTimer
);


function resetTimer() {

    timeRemaining = 90;

    timerRunning = true;

    pauseButton.textContent =
        "Pause Timer";

    updateTimerDisplay();
}