class MatchStats:
    #qb, rb1/2, wr1/2, te, d/st, flex
    #get names and points for each
    qb = []
    rb = []
    wr = []
    flex = []
    te = []
    dst = []
    team = ""
    year = 0
    week = 0

    #constructor
    def __init__(self, team, year, week):
        self.team = team
        self.year = year
        self.week = week

    #add data to the object, based off of position
    def addData(self,position, points, playerName)
        temp = [playerName, points]
        if position = "qb":
            qb.append(temp)
        elif position = "rb":
            rb.append(temp)
        elif position = "wr":
            wr.append(temp)
        elif position = "te":
            te.append(temp)
        elif position ="flex":
            flex.append(temp)
        else:
            dst.append(temp)
