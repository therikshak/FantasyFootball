from bs4 import BeautifulSoup
import pandas as pd
import requests

# start year
year = 2017
# how many weeks
week_cap = 9
# base_url just has to fill in the year
base_url = 'http://games.espn.com/ffl/schedule?leagueId=416193&seasonId={0}'

# contains an entry for every matchup result
results = []
# headers for results entries
result_header = ['Team 1 Name', 'Team 2 Name', 'Team 1 Score', 'Team 2 Score', 'Week', 'Year']

while year < 2018:
    r = requests.get(base_url.format(year))
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find('table', class_= 'tableBody')
    # increment by 10 between each week
    header_start_index = 9
    header_end_index = 11
    current_index = 2
    week_number = 1
    # get data by looping through each row
    for row in table.find_all('tr')[2:]:
        if week_number > week_cap:
            break
        match = []
        # if not in between table data
        if current_index < header_start_index:
            # get all matchup dat
            line = row.find_all('td')
            # add team 1
            match.append(line[1].text)
            # add team 2
            match.append(line[4].text)
            # split the score
            lhs, rhs = line[5].text.split("-",1)
            # add team1 score
            match.append(lhs)
            # add team2 score
            match.append(rhs)
            # add the week number
            match.append(week_number)
            # add year
            match.append(year)
            # add this match to the week list
            results.append(match)
        # once at header_end_index increment header_start, header_end, and week_number
        elif current_index == header_end_index:
            header_start_index += 10
            header_end_index += 10
            week_number += 1
        # increment current_index
        current_index += 1
        if year == 2013:
            if current_index == 131:
                break
        else:
            if current_index == 120:
                break
    year += 1
df = pd.DataFrame(results, columns=result_header)
df['Team 1 Name'] = df['Team 1 Name'].replace('','Joe Buelter')
df['Team 2 Name'] = df['Team 2 Name'].replace('','Joe Buelter')
df.to_csv('Matchup_Results.csv', index=False)
