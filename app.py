from flask import Flask, render_template, request, redirect, url_for
from python.teams import add_team, check_ready
from python.readSheet import readSheet

# Variable and class setup
app = Flask(__name__)
teams()




# Code for the home page
@app.route("/")
def home():
    sheet = readSheet("Files/TestSheet1")

    sheet.getData()

    player_data = sheet.data

    return render_template(
        "mainScreen.html",
        "teams = teams",
        "players = player_data"
    )

# Game Setup
@app.route("/setup", methods=["POST"])
def setup_Game():
    # Functionality for uploading a csv file
    file = request.form.get("player_data") # retrieves file
    sheet = readSheet() # Reads the sheet and stores it in a local variable

    # Functionality for getting the budget
    budget = request.form.get("budget_num")

    return redirect(url_for("")) # After uploading redirect to team creation


# Functionality for creating teams
@app.route("/add-team", methods=["POST"])
def create_teams():
    name = request.form.get("team_name") # Gets the team name # Gets the team name

    logo = request.form.get("logo")
    budget = request.form.get("budget")

    try:
        budget = float(budget)

        add_team(
            teams,
            name,
            logo,
            budget )

    except ValueError as error:
        return render_template(
            "mainScreen.html",
            teams=teams,
            error=str(error)
        )
    return redirect(url_for("home"))

# Drafting functionality
@app.route("/start-draft", methods=["POST"])
def start_draft():

    try:

        check_ready(teams)

    except ValueError as error:

        return render_template(
            "mainScreen.html",
            teams=teams,
            error=str(error)
        )

    return render_template(
        "mainScreen.html",
        teams=teams,
        draft_started=True
    )



# Run code
if __name__ == "__main__":
    app.run(debug=True)