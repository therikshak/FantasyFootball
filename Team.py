class Team:
    teamName = ""
    Matches = []#will contain match objects for every game in one season

    # constructor
    def __init__(self, name):
        self.teamName = name
        self.Matches = []

    #add Match
    def addMatch(self, match):
        self.Matches.append(match)
