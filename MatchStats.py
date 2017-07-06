class MatchStats:
    # qb, rb1/2, wr1/2, te, d/st, flex
    # get names and points for each
    qb = []
    rb = []
    wr = []
    te = []
    dst = []
    team = ""
    year = 0
    week = 0

    # constructor, takes in team name, year, and week and sets everything else to empty
    def __init__(self, team, year, week):
        self.team = team
        self.year = year
        self.week = week
        self.rb = []
        self.qb = []
        self.wr = []
        self.te = []
        self.dst = []

    # add data to the object, based off of position
    def addData(self,position, points, playerName):
        temp = [playerName, points]
        if position == "QB":
            self.qb = temp
        elif position == "RB":
            self.rb.append(temp)
        elif position == "WR":
            self.wr.append(temp)
        elif position == "TE":
            self.te.append(temp)
        else:
            self.dst = temp
