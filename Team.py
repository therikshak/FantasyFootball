class Team:
    teamName = ""
    # will contain match objects for every game in one season
    Matches = []
    # draft picks
    DraftPicks = []

    # constructor
    def __init__(self, name):
        self.teamName = name
        self.Matches = []
        self.DraftPicks = []

    # add Match
    def add_match(self, match):
        self.Matches.append(match)

    # add draft picks
    def add_draft_picks(self, draft):
        self.DraftPicks.append(draft)