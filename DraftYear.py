class DraftYear:
    teamName = ''
    year = ''
    picks = []

    def __init__(self, name, year):
        self.teamName = name
        self.year = year
        self.picks = []

    # add pick
    def add_pick(self, pick_num, pick_round, position, player):
        temp = [pick_num, pick_round, position, player]
        self.picks.append(temp)