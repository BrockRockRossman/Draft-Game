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






