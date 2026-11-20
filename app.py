# Header: This is the code for the flask for the webapplication. This integrates the functionality of our code with the
# html code


from flask import Flask, render_template, request, redirect, url_for, session
from python.readSheet import readSheet
from python.teams import Team, Player
from python.Draft import Draft


# Variable and class setup
app = Flask(__name__)

# Setup Variables
sheet = readSheet

mainDraft = Draft

budget = 0
players = []
teams = []

# I tried to organize the routes in the order that one might see them in, starting with the setup page submit



# ---------------------------- SETUP ----------------------------



# setup page submit button
@app.route("/setup", methods=["POST"])
def setup_Game():
    # Setup retrieval
    file = request.form.get("player_data") # retrieves file
    budget = request.form.get("budget_num") # Functionality for getting the budget
    session['budget'] = budget


    sheet = readSheet(file)


    return redirect(url_for("setup2.html")) # After uploading redirect to team setup page

# Functionality for button to create a new team
@app.route("/add-team", methods=["POST"])
def create_teams():

    name = request.form.get("team_name") # Gets the team name
    logo = request.form.get("logo") # Gets the uploaded logo
    budget = session.get('budget')
    new_team = Team(name, logo, budget) # Creates a team object with the parameters
    teams.append(new_team) # Adds the team to the teams list

    return render_template("setup.html", teams = teams) # Renders the setup page again with the updated teams list
    # In html, get the teams list in order to display the teams already made

@app.route("/fin-team", methods=["POST"])
def submit_teams():

        mainDraft = Draft(teams, players, 10) # !!! currently not referencing the mainDraft outside of the method, needs fixing

        return redirect("mainScreen.html")



# ---------------------------- Home Page ----------------------------



# Code for the home page
@app.route("/")
def home():
    sheet = readSheet("Files/TestSheet1")

    sheet.getData()

    player_data = sheet.data

    return render_template(
        "mainScreen.html",
        teams = teams, players = player_data)



# ---------------------------- Draft Page ----------------------------

# Drafting code
@app.route("/draft", methods=["POST"])
def draft_pick():
    player_num = request.form.get("player_num") # Retrieves the player number entered for the draft

    cur_team = mainDraft.current_team() # Retrieves which team is currently drafting

# Functiuonality for the undo button
@app.route("/undo", methods=["POST"])
def undo():
    mainDraft.undo_pick() # Undoes the pick

    cur_team = mainDraft.current_team() # Retrieves the current team

    render_template() # Re renders html with updated current team information






# Run code
if __name__ == "__main__":
    app.run(debug=True)