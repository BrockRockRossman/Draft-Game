# Header: This is the code for the flask for the webapplication. This integrates the functionality of our code with the
# html code

import os

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from python.teams import Team, Player
from python.readSheet import readSheet
from python.Draft import Draft, add_team, check_ready, draft_order

# Variable and class setup
app = Flask(__name__)

# Setup Variables
teams = []                    # Team objects created on createTeams.html
players = []                  # Player objects loaded from the uploaded CSV
mainDraft = None              # Draft object after the game is started
uploaded_filename = None      # Name shown on the welcome page after upload
ROUNDS = 10                   # The project uses a 10-round draft
ALLOWED_EXTENSIONS = {"csv"}  # Only CSV uploads are accepted

#file cvs readers method

def allowed_file(filename):
    """Return True only when the uploaded file has an allowed extension"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

#Reads the upload file and convert each data row into a Player object so it is pass to mainScreen and availablePlayer
def load_players_from_csv(file_path):

    # Use our readSheet class
    sheet = readSheet(file_path)

    # Call the team's getData() method. It returns the CSV as a list of rows.
    rows = sheet.getData()

    # Do not continue if the uploaded CSV is empty.
    if not rows:
        raise ValueError(
            "The CSV does not contain any data"
        )
    # The first CSV row contains the column names.
    # strip() removes accidental spaces around a header name.
    headers = [
        header.strip()
        for header in rows[0]
    ]
    #construct a player object
    required = {
        "ID",
        "FirstName",
        "LastName",
        "Price"
    }
    #if statement to verify all required columns are present
    if not required.issubset(set(headers)):

        raise ValueError(
            "CSV must contain ID, FirstName, "
            "LastName, and Price columns"
        )

    loaded_players = []

    # Everything after first row = players
    for values in rows[1:]:

        # Skip blank rows
        if not values:
            continue

     # Convert the row from a list into a dictionary using the CSV headers.
        row = dict(
            zip(headers, values)
        )

        try:
            # Build the full player name from the first and last name columns.
            name = (
                f"{row['FirstName']} "
                f"{row['LastName']}"
            ).strip()
            #player's id
            number = int(
                row["ID"]
            )
            #price for each player
            price = float(
                row["Price"]
            )

        except (ValueError, TypeError, KeyError):
            # This catches missing columns or non-numeric ID/price values.
            raise ValueError(
                "Invalid player data in CSV"
            )

        # The current test CSV stores values such as 10000 while the website
        # displays game budgets/prices on a smaller scale. 10000 becomes 10.
        if price > 1000:
            price = price / 1000

        player = Player(
            name,
            number,
            price
        )

        # Add Stat1, Stat2, Stat3, Stat4, etc.
        for key, value in row.items():

            if key not in required:

                setattr(
                    player,
                    key.lower(),
                    value
                )

        loaded_players.append(player)

    if not loaded_players:

        raise ValueError(
            "The CSV does not contain any players"
        )

    return loaded_players

#Build the rows/cells that draftBoard.html displays
def board_rows():
    # With no teams, nothing to display.
    if not teams:
        return []

    # Before the draft starts, show the planned snake order.
    if mainDraft is None:
        turn_order = draft_order(teams, ROUNDS)
        picked_players = []
        active_index = None

    # Once the draft starts, uses the real draft order.
    else:
        turn_order = mainDraft.turn_order
        picked_players = mainDraft.picked_players

        # The next index after the completed picks is the active square

        if len(picked_players) < len(turn_order):
            active_index = len(picked_players)
        else:
            active_index = None

    rows = []

    # Create one board row for each draft round.
    for round_index in range(ROUNDS):

        cells = []

        # Each team gets one turn/cell in each round.
        for turn_index in range(len(teams)):

            # Convert round + turn into the overall draft-pick index.
            overall_index = (
                round_index * len(teams)
                + turn_index
            )
            # The team for this cell comes from the Python snake turn order.
            team = turn_order[overall_index]

            # A cell has no player until that overall pick has happened.
            player = None

            if overall_index < len(picked_players):
                player = picked_players[overall_index]

            cells.append({
                "team": team,
                "player": player,
                "overall_index": overall_index,
                "active": overall_index == active_index,
            })

        rows.append({
            "round_number": round_index + 1,
            "cells": cells,
        })

    return rows


# WELCOME / SETUP

#Display the welcome/setup page.
@app.route("/")
def welcome():
    return render_template(
        "welcome.html",
        upload_success=request.args.get("upload_success") == "1",
        upload_error=request.args.get("upload_error"),
        uploaded_filename=uploaded_filename,
    )

#Receive the CSV submitted by the form on welcome.html.
@app.route("/upload-file", methods=["POST"])
def upload_file():

    global players, uploaded_filename

    uploaded_file = request.files.get(
        "player_data"
    )

    if (
        uploaded_file is None
        or uploaded_file.filename == ""
    ):
        return redirect(
            url_for(
                "welcome",
                upload_error=
                "Please choose a CSV file first."
            )
        )

    if not allowed_file(
        uploaded_file.filename
    ):
        return redirect(
            url_for(
                "welcome",
                upload_error=
                "Only .csv files are accepted."
            )
        )

    filename = secure_filename(
        uploaded_file.filename
    )

    files_folder = os.path.join(
        app.root_path,
        "Files"
    )

    os.makedirs(
        files_folder,
        exist_ok=True
    )

    file_path = os.path.join(
        files_folder,
        filename
    )

    # Save uploaded CSV
    uploaded_file.save(
        file_path
    )

    try:

        # This now eventually calls:
        # readSheet.getData()
        players = load_players_from_csv(
            file_path
        )

    except (ValueError, TypeError) as error:

        return redirect(
            url_for(
                "welcome",
                upload_error=str(error)
            )
        )

    uploaded_filename = filename

    return redirect(
        url_for(
            "welcome",
            upload_success="1"
        )
    )

#Display the page where the admin creates 3-5 teams.
@app.route("/create-teams")
def create_teams_page():
    return render_template(
        "createTeams.html",
        teams=teams,
        error=request.args.get("error"),
        uploaded_filename=uploaded_filename,
    )

#Receive one team from the Create Teams form and add it with add_team().
@app.route("/add-team", methods=["POST"])
def create_team():
    name = request.form.get("team_name", "").strip()
    logo = request.form.get("logo", "").strip()
    budget_text = request.form.get("budget", "").strip()

    try:
        if not name:
            raise ValueError("Team name is required")

        budget = float(budget_text)
        add_team(teams, name, logo, budget)

    except (ValueError, TypeError) as error:
        return redirect(url_for("create_teams_page", error=str(error)))

    return redirect(url_for("create_teams_page"))

#Validate setup and create the single Draft object used by the game.
@app.route("/start-draft", methods=["POST"])
def start_draft():
    global mainDraft, current_pick_index

    try:
        # Reuse the team's Python validation: at least 3 teams are required.
        check_ready(teams)

        # The game cannot start without player data from the CSV upload.
        if not players:
            raise ValueError("Upload a valid player CSV before starting the draft")

        mainDraft = Draft(teams, list(players), ROUNDS)

    except ValueError as error:
        return redirect(url_for("create_teams_page", error=str(error)))

    return redirect(url_for("dashboard"))


# MAIN APPLICATION PAGES

#Render the main dashboard using the current Python draft state.
@app.route("/dashboard")
def dashboard():

    # get_draft_state() centralizes values shared by dashboard and draft board.
    state = get_draft_state()

    available_players = (
        mainDraft.available
        if mainDraft is not None
        else players
    )

    return render_template(
        "mainScreen.html",
        teams=teams,
        players=available_players,

        current_team=state["current_team"],
        current_pick=state["current_pick"],
        round_number=state["round_number"],
        picks_done=state["picks_done"],
        total_picks=state["total_picks"],
        draft_complete=state["draft_complete"],

        revealed=request.args.get("revealed"),
        error=request.args.get("error"),
    )


#Display each team's current budget and drafted roster.
@app.route("/teams")
def teams_page():
    return render_template("teams.html", teams=teams)

#Display only players that are still available to draft.
@app.route("/players")
def players_page():
    available = mainDraft.available if mainDraft is not None else players
    return render_template("availablePlayers.html", players=available)

#Render the visual draft board from the same draft state as dashboard.
@app.route("/draft-board")
def draft_board():

    state = get_draft_state()

    return render_template(
        "draftBoard.html",
        teams=teams,
        board_rows=board_rows(),

        current_team=state["current_team"],
        current_pick=state["current_pick"],
        round_number=state["round_number"],
        picks_done=state["picks_done"],
        total_picks=state["total_picks"],
        draft_complete=state["draft_complete"],

        rounds=ROUNDS,
    )
# DRAFT ACTIONS

@app.route("/draft", methods=["POST"])
def draft_pick():
#Draft the player ID submitted from the dashboard form
# Do not allow a player pick until start_draft() created the Draft object.
    if mainDraft is None:
        return redirect(url_for("dashboard"))

    player_num = request.form.get(
        "player_num",
        ""
    ).strip()

    try:
        player = mainDraft.pick_player(
            int(player_num)
        )

    except (ValueError, TypeError) as error:
        return redirect(
            url_for(
                "dashboard",
                error=str(error)
            )
        )
#Reset_timer=1 is read by static/script.js. It tells JavaScript that a
#successful pick happened and the next team should reset the timer
    return redirect(
        url_for(
            "dashboard",
            revealed=player.name,
            reset_timer=1
        )
    )

@app.route("/next-pick", methods=["POST"])
def next_pick():
    global current_pick_index

    if teams:
        last_index = len(teams) * ROUNDS - 1
        current_pick_index = min(current_pick_index + 1, last_index)

    return redirect(request.referrer or url_for("dashboard"))

#Undo the most recent successful player pick.
@app.route("/undo", methods=["POST"])
def undo():

    if mainDraft is not None:
        try:
            # Draft.undo_pick() restores the player's team budget, roster,
            # availability, and team assignment in one Python method.
            mainDraft.undo_pick()

        except ValueError:
            pass

    return redirect(
        request.referrer
        or url_for("dashboard")
    )

def get_draft_state():
    """Return the current draft information used by both
    the dashboard and the draft board.
    """
    if mainDraft is None:
        return {
            "current_team": None,
            "current_pick": 1,
            "round_number": 1,
            "picks_done": 0,
            "total_picks": len(teams) * ROUNDS,
            "draft_complete": False,
        }

    picks_done = len(mainDraft.picked_players)
    total_picks = len(mainDraft.turn_order)

    draft_complete = picks_done >= total_picks

    if draft_complete:
        current_team = None
        current_pick = total_picks
        round_number = ROUNDS
    else:
        current_team = mainDraft.current_team()
        current_pick = picks_done + 1
        round_number = (picks_done // len(teams)) + 1

    return {
        "current_team": current_team,
        "current_pick": current_pick,
        "round_number": round_number,
        "picks_done": picks_done,
        "total_picks": total_picks,
        "draft_complete": draft_complete,
    }

if __name__ == "__main__":
    app.run(debug=True)
