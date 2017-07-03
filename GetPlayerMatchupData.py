from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests
import copy
from MatchStats import MatchStats
from Team import Team

#teamId by index for other years
teamIDs = ['Erik Stryshak', 'Charlie Frank', "Brendan Hart",
            'Stefan Hanish', 'Andrew McDowell', 'Horlacher',
            'Geoffrey Raclin', 'Trey Shmo', 'Richard Graney',
            'Tommy Stupp', 'Peter Condie', 'James Carman',
            'Chandler Dalton', 'Ozair Ferozuddin']
# 0 is teamId, add 1 for url
# 1 is week, 2013 had 13 weeks, every other season had 12
# 2 is year 2013-2016 for now
baseURL = 'http://games.espn.com/ffl/boxscorequick?leagueId=416193&teamId={0}&scoringPeriodId={1}&seasonId={2}&view=scoringperiod&version=quick'

years = [2013, 2014, 2015, 2016]
weeks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
teamId = 1
teamData = []
for team in teamIDs:
    tempTeam = Team(team)
    for year in years:
        for week in weeks:
            if year == 2013 or (year > 2013 and week != 13):
                r = requests.get(baseURL.format(teamId, week, year))
                soup = BeautifulSoup(r.text, 'html.parser')
                table = soup.find('table', class_='playerTableTable tableBody')
                tempMatch = MatchStats(team, year, week)
                #loop through players of one team's match
                for row in table.find_all('tr')[3:11]:
                    # get all matchup data
                    line = row.find_all('td')
                    if year < 2016:
                        if line[0].text == "Total":
                            break
                        else:
                            # split player name from other text
                            playerName, rhs = line[0].text.split(",", 1)
                            # get position
                            position = rhs[-2:]
                            #get players points
                            if line[1].text == '** BYE **':
                                points = line[2].text
                            else:
                                points = line[3].text
                            tempMatch.addData(position, points, playerName)
                    else:
                        position = line[0].text
                        errRaise = False
                        try:
                            playerName = line[1].find('a').text
                        except AttributeError:
                            #this error gets raised if there is a blank roster spot
                            playerName = ''
                            errRaise = True
                        if errRaise:
                            points = 0
                        elif line[2].text == '** BYE **':
                            points = line[3].text
                        else:
                            points = line[4].text
                        tempMatch.addData(position, points, playerName)

                tempTeam.addMatch(tempMatch)
    teamId += 1
    teamData.append(tempTeam)
