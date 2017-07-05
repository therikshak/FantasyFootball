from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests
import copy
from MatchStats import MatchStats
from Team import Team
import csv
import os

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
#for team in teamIDs:
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

#df.to_csv('results.csv', index=False)
#output data to csv
#one csv per team
#YEAR WEEK TEAMNAME QBNAME QBSCORE RBNAME RBSCORE ...TOTAL POINTS
rHeader = ['YEAR', 'WEEK', 'TEAM_NAME', 'QB_NAME', 'QB_SCORE',
            'RB_NAME', 'RB_SCORE','RB_NAME', 'RB_SCORE','WR_NAME',
            'WR_SCORE', 'WR_NAME', 'WR_SCORE', 'TE_NAME', 'TE_SCORE',
            'DST_NAME', 'DST_SCORE','FLEX_NAME','FLEX_POS', 'FLEX_SCORE']


for team in teamData:
    outName = team.teamName + '.csv'
    with open(outName, 'w', newline='') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(rHeader)
        for match in team.Matches:
            line = [match.year, match.week, match.team]

            #add qb
            try:
                line.append(match.qb[0])
                line.append(match.qb[1])
            except IndexError:
                line.append('n/a')
                line.append(0)

            #add rb1
            try:
                line.append(match.rb[0][0])
                line.append(match.rb[0][1])
            except IndexError:
                line.append('n/a')
                line.append(0)
            #add rb2
            try:
                line.append(match.rb[1][0])
                line.append(match.rb[1][1])
            except IndexError:
                line.append('n/a')
                line.append(0)

            #add wr1
            try:
                line.append(match.wr[0][0])
                line.append(match.wr[0][1])
            except IndexError:
                line.append('n/a')
                line.append(0)
            #add wr2
            try:
                line.append(match.wr[1][0])
                line.append(match.wr[1][1])
            except IndexError:
                line.append('n/a')
                line.append(0)

            #add tight end
            try:
                line.append(match.te[0][0])
                line.append(match.te[0][1])
            except IndexError:
                line.append('n/a')
                line.append(0)

            #add defense
            try:
                line.append(match.dst[0])
                line.append(match.dst[1])
            except IndexError:
                line.append('n/a')
                line.append(0)

            #add the flex
            try: #try the rb first
                line.append(match.rb[2][0])
                line.append('rb')
                line.append(match.rb[2][1])
            except IndexError:
                try: #if error, try the wr
                    line.append(match.wr[2][0])
                    line.append('wr')
                    line.append(match.wr[2][1])
                except IndexError:
                    try: #if error try te
                        line.append(match.te[1][0])
                        line.append('te')
                        line.append(match.te[1][1])
                    except IndexError: #if error, null
                        line.append('n/a')
                        line.append('n/a')
                        line.append(0)
            #write the line to the csv file
            csv_out.writerow(line)
