// ======================================================
// SHARED DRAFT TIMER
// Used by mainScreen.html and draftBoard.html
// ======================================================

const TIMER_LENGTH = 90;


// Dashboard timer
const dashboardTimer =
    document.getElementById("timer");


// Draft board timer
const boardTimer =
    document.getElementById("draftBoardTimer");


// Dashboard control buttons
const pauseButton =
    document.getElementById("pauseButton");

const resetButton =
    document.getElementById("resetButton");


// ------------------------------------------------------
// Initialize timer storage
// ------------------------------------------------------

if (localStorage.getItem("draftTimerRemaining") === null) {

    localStorage.setItem(
        "draftTimerRemaining",
        TIMER_LENGTH
    );

    localStorage.setItem(
        "draftTimerRunning",
        "true"
    );

    localStorage.setItem(
        "draftTimerEnd",
        Date.now() + TIMER_LENGTH * 1000
    );
}


// ------------------------------------------------------
// GET REMAINING TIME
// ------------------------------------------------------

function getRemainingTime() {

    const running =
        localStorage.getItem("draftTimerRunning") === "true";

    if (!running) {

        return Number(
            localStorage.getItem("draftTimerRemaining")
        );
    }


    const endTime =
        Number(
            localStorage.getItem("draftTimerEnd")
        );


    const remaining =
        Math.ceil(
            (endTime - Date.now()) / 1000
        );


    return Math.max(0, remaining);
}


// ------------------------------------------------------
// SAVE REMAINING TIME
// ------------------------------------------------------

function saveRemainingTime(seconds) {

    localStorage.setItem(
        "draftTimerRemaining",
        seconds
    );
}


// ------------------------------------------------------
// DISPLAY TIMER
// ------------------------------------------------------

function displayTimer() {

    const remaining =
        getRemainingTime();


    const minutes =
        Math.floor(remaining / 60);


    const seconds =
        remaining % 60;


    const formatted =
        String(minutes).padStart(2, "0")
        +
        ":"
        +
        String(seconds).padStart(2, "0");


    // Dashboard
    if (dashboardTimer) {
        dashboardTimer.textContent = formatted;
    }


    // Draft board
    if (boardTimer) {
        boardTimer.textContent = formatted;
    }


    saveRemainingTime(remaining);


    // Stop timer at zero
    if (remaining <= 0) {

        localStorage.setItem(
            "draftTimerRunning",
            "false"
        );

        updatePauseButton();
    }
}


// ------------------------------------------------------
// UPDATE PAUSE BUTTON
// ------------------------------------------------------

function updatePauseButton() {

    if (!pauseButton) {
        return;
    }


    const running =
        localStorage.getItem("draftTimerRunning") === "true";


    pauseButton.textContent =
        running
            ? "Pause Timer"
            : "Resume Timer";
}


// ------------------------------------------------------
// RESET TIMER
// ------------------------------------------------------

function resetTimer() {

    localStorage.setItem(
        "draftTimerRemaining",
        TIMER_LENGTH
    );

    localStorage.setItem(
        "draftTimerRunning",
        "true"
    );

    localStorage.setItem(
        "draftTimerEnd",
        Date.now() + TIMER_LENGTH * 1000
    );


    displayTimer();

    updatePauseButton();
}


// ------------------------------------------------------
// PAUSE / RESUME TIMER
// ------------------------------------------------------

function toggleTimer() {

    const running =
        localStorage.getItem("draftTimerRunning") === "true";


    // PAUSE
    if (running) {

        const remaining =
            getRemainingTime();


        localStorage.setItem(
            "draftTimerRemaining",
            remaining
        );


        localStorage.setItem(
            "draftTimerRunning",
            "false"
        );
    }


    // RESUME
    else {

        let remaining =
            Number(
                localStorage.getItem(
                    "draftTimerRemaining"
                )
            );


        // If timer reached zero,
        // restart at 90 seconds
        if (remaining <= 0) {
            remaining = TIMER_LENGTH;
        }


        localStorage.setItem(
            "draftTimerRunning",
            "true"
        );


        localStorage.setItem(
            "draftTimerEnd",
            Date.now() + remaining * 1000
        );
    }


    displayTimer();

    updatePauseButton();
}


// ------------------------------------------------------
// BUTTON EVENTS
// ------------------------------------------------------

if (pauseButton) {

    pauseButton.addEventListener(
        "click",
        toggleTimer
    );
}


if (resetButton) {

    resetButton.addEventListener(
        "click",
        resetTimer
    );
}


// ------------------------------------------------------
// AUTOMATIC RESET AFTER SUCCESSFUL PICK
//
// Flask redirects to:
// /dashboard?reset_timer=1
// ------------------------------------------------------

const urlParams =
    new URLSearchParams(
        window.location.search
    );


if (urlParams.get("reset_timer") === "1") {

    resetTimer();


    // Remove reset_timer so refreshing the page
    // does not reset the timer again.
    urlParams.delete("reset_timer");


    const cleanUrl =
        window.location.pathname
        +
        (
            urlParams.toString()
                ? "?" + urlParams.toString()
                : ""
        );


    window.history.replaceState(
        {},
        "",
        cleanUrl
    );
}


// ------------------------------------------------------
// INITIAL DISPLAY
// ------------------------------------------------------

displayTimer();

updatePauseButton();


// ------------------------------------------------------
// UPDATE SCREEN EVERY 250ms
// ------------------------------------------------------

setInterval(
    displayTimer,
    250
);


// ------------------------------------------------------
// SYNC IF ANOTHER TAB CHANGES TIMER
// ------------------------------------------------------

window.addEventListener(
    "storage",
    () => {

        displayTimer();

        updatePauseButton();
    }
);
// ======================================================
// WELCOME PAGE - CSV FILE NAME DISPLAY
//
// HTML connections:
// id="player_data" -> CSV file input
// id="fileLabel"   -> text shown inside Choose CSV button
//
// This only displays the selected file name.
// Flask/app.py handles the actual upload and readSheet.py
// handles reading the CSV.
// ======================================================

const fileInput =
    document.getElementById("player_data");

const fileLabel =
    document.getElementById("fileLabel");


if (fileInput && fileLabel) {

    fileInput.addEventListener(
        "change",
        () => {

            fileLabel.textContent =
                fileInput.files.length
                    ? fileInput.files[0].name
                    : "CHOOSE CSV";
        }
    );
}
// ======================================================
// DRAFT PROGRESS BAR
//
// HTML connection:
// id="progressBar" in mainScreen.html
//
// Flask sends picks_done and total_picks into the HTML
// using data-* attributes.
//
// JavaScript reads those values and calculates the
// percentage width of the progress bar.
// ======================================================

const progressBar =
    document.getElementById("progressBar");


if (progressBar) {

    const picksDone =
        Number(
            progressBar.dataset.picksDone || 0
        );


    const totalPicks =
        Number(
            progressBar.dataset.totalPicks || 0
        );


    let progressPercent = 0;


    if (totalPicks > 0) {

        progressPercent =
            (picksDone / totalPicks) * 100;
    }


    progressBar.style.width =
        progressPercent + "%";
}

