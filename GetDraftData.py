from bs4 import BeautifulSoup
import requests
from DraftYear import DraftYear
from Team import Team
import csv

baseURL = "http://games.espn.com/ffl/tools/draftrecap?leagueId=416193&seasonId={0}&mode=1"

years = [2013, 2014, 2015, 2016]
teamIDs = ['Erik Stryshak', 'Charlie Frank', "Brendan Hart",
            'Stefan Hanish', 'Andrew McDowell', 'Horlacher',
            'Geoffrey Raclin', 'Trey Shmo', 'Richard Graney',
            'Tommy Stupp', 'Peter Condie', 'James Carman',
            'Chandler Dalton', 'Ozair Ferozuddin']

# list to store team objects
teamData = []

#initialize team objects
for t in teamIDs:
    temp = Team(t)
    teamData.append(temp)

# loop through tables containing the team's draft picks
for year in years:
    # get the url with formatting
    r = requests.get(baseURL.format(year))
    # use BeautifulSoup to get the webpage
    soup = BeautifulSoup(r.text, 'html.parser')
    # get all tables
    tables = soup.find_all('table')

    teamIndex = 0
    for table in tables[2:16]:
        roundNumber = 1

        # create draft data object
        draft = DraftYear(teamIDs[teamIndex], year)

        for row in table.find_all('tr')[1:15]:
            # get data in the row
            line = row.find_all('td')

            # get the draft pick number
            pickNum = line[0].text

            if year == 2016:
                playerName = line[1].find('a').text
                position = line[1].text[-2:]
            else:
                playerName, rhs = line[1].text.split(",", 1)
                position = rhs[-2:]

            # add data to draft year object
            draft.addPick(pickNum, roundNumber, position, playerName)

            # increment roundNumber
            roundNumber += 1

        # add team to teamData list
        teamData[teamIndex].addDraftPicks(draft)
        teamIndex += 1

# header for csv file
draftHeader = ['Year', 'Team', 'Round', 'Pick', 'Position', 'Player']
# output data to a csv
with open('Draft.csv', 'w', newline='') as out:
    # create a csv writer
    csv_out = csv.writer(out)
    # write the header to the csv file
    csv_out.writerow(draftHeader)
    for team in teamData:
        for draft in team.DraftPicks:
            outLine = [draft.year, draft.teamName, 0, 0, '', '']
            for pick in draft.picks:
                outLine[2] = pick[1]
                outLine[3] = pick[0]
                outLine[4] = pick[2]
                outLine[5] = pick[3]
                csv_out.writerow(outLine)