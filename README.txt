Classes
	DraftYear.py
		-Contains: team name, year, list of picks
		-each pick contains the pick #, pick round, position, player name
	Team.py
		-Contains: team name, list of MatchStats objects and a list of DraftYear objects
	MatchStats.py
		-contains team name, year, week, and a list of each position
		-each position list contains a list with the player name and their points scored
Programs
	FantasyFootballScraping.py: WEEKLY UPDATE 1
		-Outputs CSV with total team matchup results (no players)
		-Change Year and # of Weeks at top of file
		-Copy Paste CSV to Excel file
	GetPLayerMatchupData.py: WEEKLY UPDATE 2
		-Outputs CSV with matchup results containing each player's score
		-Change years and weeks lists
	CombineTeamData.py WEEKLY UPDATE 3
		-Combines each individual teams data(player scores by week) into one csv file named 'All_Team_Matchups.csv'
	CalculateRankings.py
		-NOT COMPLETE