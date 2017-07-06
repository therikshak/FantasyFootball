class DraftYear:
    teamName = ''
    year = ''
    picks = []

    def __init__(self, name, year):
        self.teamName = name
        self.year = year
        self.picks = []

    # add pick
    def addPick(self, pickNum, pickRound, position, player):
        temp = [pickNum, pickRound, position, player]
        self.picks.append(temp)