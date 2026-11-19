BUDGET_CAP = 1000  # number: the most money a team can ever have


# class (blueprint) for one team. every Team(...) made from it is an object
class Team:
    def __init__(self, name, logo, budget):
        self.name = name      # text
        self.logo = logo      # text
        self.budget = budget  # number
        self.roster = []      # list of Player objects this team has picked


# class (blueprint) for one player. every Player(...) made from it is an object
class Player:
    def __init__(self, name, number, price):
        self.name = name      # text
        self.number = number  # number, used to pick them
        self.price = price    # number
        self.team = None      # the Team object that picked them (None = not picked yet)


# adds a team to the teams list if it follows the rules
# teams is a list of Team objects, made outside this file with teams = [] (see test_draft.py)
def add_team(teams, name, logo, budget):
    if len(teams) >= 5:
        raise ValueError("You can't have more than 5 teams")
    for team in teams:  # team = each Team object already in the list
        if team.name.lower() == name.lower():
            raise ValueError("That team name is already used")
    if budget <= 0:
        raise ValueError("Budget must be above 0")
    if budget > BUDGET_CAP:
        raise ValueError("Budget can't be more than the cap")
    new_team = Team(name, logo, budget)  # makes a new Team object
    teams.append(new_team)               # adds it to the end of the teams list
    return new_team


# checks there are enough teams to start (app.py calls this when "Start draft" is clicked)
def check_ready(teams):
    if len(teams) < 3:
        raise ValueError("You need at least 3 teams to start")


# makes the snake order: a list of Team objects, one for every turn
# like [Bears, Lions, Packers, Packers, Lions, Bears, Bears, ...]
def draft_order(teams, rounds=10):
    forward = teams                   # list: [Bears, Lions, Packers]
    backward = list(reversed(teams))  # list: [Packers, Lions, Bears]

    turn_order = []  # list, starts empty and gets one round added each loop
    for r in range(rounds):  # r is the round number: 0, 1, 2 ... 9
        if r % 2 == 0:
            turn_order = turn_order + forward    # even rounds (0, 2, 4...)
        else:
            turn_order = turn_order + backward   # odd rounds (1, 3, 5...)
    return turn_order


# class (blueprint) for the draft. Draft(...) makes one draft object that remembers everything
class Draft:
    def __init__(self, teams, players, rounds=10):
        check_ready(teams)  # need at least 3 teams
        self.teams = teams                           # LIST of Team objects
        self.available = players                     # LIST of Player objects nobody has picked yet
        self.turn_order = draft_order(teams, rounds)  # LIST of Team objects: whose turn each spot is
        self.picked_players = []                     # LIST of Player objects, in the order they were picked

    # finds the Team object whose turn it is
    def current_team(self):
        picks_done = len(self.picked_players)  # NUMBER: how many picks have happened
        total_turns = len(self.turn_order)     # NUMBER: how many turns the whole draft has
        if picks_done >= total_turns:
            raise ValueError("The draft is over")
        next_spot = picks_done                 # NUMBER: the spot of the next turn (0 picks done = spot 0)
        team = self.turn_order[next_spot]      # Team object at that spot
        return team

    # picks a player by their number for the team whose turn it is
    def pick_player(self, number):
        # look through the available list for the player with that number
        player = None
        for p in self.available:  # p = each Player object still available
            if p.number == number:
                player = p
        if player is None:
            raise ValueError("That player is already picked or doesn't exist")

        team = self.current_team()  # Team object whose turn it is
        if player.price > team.budget:
            raise ValueError("Not enough budget")

        team.budget = team.budget - player.price
        team.roster.append(player)         # adds the player to the team's roster list
        player.team = team                 # the player remembers which team picked them
        self.available.remove(player)      # takes the player out of the available list
        self.picked_players.append(player)  # adds the player to the picked list (used for undo)
        return player

    # undoes the last pick: player goes back and the team gets its money back
    def undo_pick(self):
        if len(self.picked_players) == 0:
            raise ValueError("There's nothing to undo")
        player = self.picked_players.pop()  # takes the last Player object off the picked list
        team = player.team                  # the Team object that picked them
        team.budget = team.budget + player.price
        team.roster.remove(player)          # takes the player off the roster list
        player.team = None                  # the player isn't on a team anymore
        self.available.append(player)       # puts the player back in the available list
        # the picked list got smaller, so it goes back to that team's turn

    # one team sends money to another (giver and receiver are Team objects)
    def trade_money(self, giver, receiver, amount):
        if amount <= 0:
            raise ValueError("Amount must be above 0")
        if amount > giver.budget:
            raise ValueError("Not enough budget")
        new_budget = receiver.budget + amount  # NUMBER: what the receiver would have after
        if new_budget > BUDGET_CAP:
            raise ValueError("That would put the team over the cap")
        giver.budget = giver.budget - amount
        receiver.budget = receiver.budget + amount

    # trades a turn in the turn order, not a player
    # spot is a NUMBER for a place in the turn order (starts at 0), giver and receiver are Team objects
    def trade_pick(self, spot, giver, receiver):
        picks_done = len(self.picked_players)  # NUMBER: how many picks have happened
        if spot < picks_done:
            raise ValueError("That pick already happened")
        owner = self.turn_order[spot]          # Team object that owns that spot right now
        if owner != giver:
            raise ValueError("That team doesn't own that pick")
        self.turn_order[spot] = receiver       # puts the receiver in that spot
