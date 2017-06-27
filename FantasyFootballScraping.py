from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests

#start at year 2013
year = 2013
#baseURL just has to fill in the year
baseURL = 'http://games.espn.com/ffl/schedule?leagueId=416193&seasonId={0}'

#contains an entry for every matchup result
results = []
#headers for results entries
resultHeader = ['Team 1 Name', 'Team 2 Name', 'Team 1 Score', 'Team 2 Score', 'Week', 'Year']

while year < 2017:
    r = requests.get(baseURL.format(year))
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find('table', class_= 'tableBody')
    #increment by 10 between each week
    headerStartIndex = 9
    headerEndIndex = 11
    currentIndex = 2
    weekNum = 1
    #get data by looping through each row
    for row in table.find_all('tr')[2:]:
        match = []
        #if not in between table data
        if currentIndex < headerStartIndex :
            #get all matchup dat
            line = row.find_all('td')
            #add team 1
            match.append(line[1].text)
            #add team 2
            match.append(line[4].text)
            #split the score
            lhs, rhs = line[5].text.split("-",1)
            #add team1 score
            match.append(lhs)
            #add team2 score
            match.append(rhs)
            #add the week number
            match.append(weekNum)
            #add year
            match.append(year)
            #add this match to the week list
            results.append(match)
        #once at headerEndIndex increment headerstart, headerend, and weekNum
        elif currentIndex == headerEndIndex:
            headerStartIndex += 10
            headerEndIndex += 10
            weekNum += 1
        #increment currentIndex
        currentIndex += 1
        if year == 2013:
            if currentIndex == 131:
                break
        else:
            if currentIndex == 120:
                break
    year += 1
df = pd.DataFrame(results, columns = resultHeader)
df['Team 1 Name'] = df['Team 1 Name'].replace('','Joe Buelter')
df['Team 2 Name'] = df['Team 2 Name'].replace('','Joe Buelter')
df.to_csv('results.csv', index=False)
