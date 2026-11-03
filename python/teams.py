class Team:
    def __init__(self, name, logo, budget):
        self.name = name
        self.logo = logo
        self.budget = budget
        self.roster = []

    def to_dict(self):
        return {"name": self.name, "logo": self.logo, "budget": self.budget}


def add_team(all_teams, name, logo, budget):
    if len(all_teams) >= 5:
        raise ValueError("You can't have more than 5 teams")
    for t in all_teams.values():
        if t.name.lower() == name.lower():
            raise ValueError("That team name is already used")
    if budget <= 0:
        raise ValueError("Budget must be above 0")

    number = len(all_teams) + 1
    all_teams[number] = Team(name, logo, budget)
    return all_teams[number]


def check_ready(all_teams):
    if len(all_teams) < 3:
        raise ValueError("You need at least 3 teams to start")
