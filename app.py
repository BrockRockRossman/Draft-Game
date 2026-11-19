from flask import Flask, render_template

app = Flask(__name__)

teams = {}
players = []


@app.route("/")
@app.route("/dashboard")
def dashboard():
    return render_template(
        "mainScreen.html",
        teams=teams,
        players=players
    )


@app.route("/teams")
def teams_page():
    return render_template(
        "teams.html",
        teams=teams
    )


@app.route("/players")
def players_page():
    return render_template(
        "availablePlayers.html",
        players=players
    )


@app.route("/draft-board")
def draft_board():
    return render_template(
        "draftBoard.html",
        teams=teams
    )


if __name__ == "__main__":
    app.run(debug=True)