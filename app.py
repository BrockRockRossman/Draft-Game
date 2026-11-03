from flask import Flask, render_template, request, redirect, url_for
from teams import add_team, check_ready
from readSheet import readSheet

app = Flask(__name__)

teams()

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
@app.route("/add-team", methods=["POST"])

def create_teams():
    name = request.form.get("team_name")
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

if __name__ == "__main__":
    app.run(debug=True)