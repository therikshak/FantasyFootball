from bs4 import BeautifulSoup
import requests
from MatchStats import MatchStats
from Team import Team
import csv

# team_ID by index
team_IDs = ['Erik Stryshak', 'Charlie Frank', "Brendan Hart",
            'Stefan Hanish', 'Andrew McDowell', 'Horlacher',
            'Geoffrey Raclin', 'Trey Shmo', 'Richard Graney',
            'Tommy Stupp', 'Peter Condie', 'James Carman',
            'Chandler Dalton', 'Ozair Ferozuddin']

# 0 is team_ID, add 1 for url
# 1 is week, 2013 had 13 weeks, every other season had 12
# 2 is year 2013-2016 for now
base_url = 'http://games.espn.com/ffl/boxscorequick?leagueId=416193&teamId={0}&scoringPeriodId={1}&seasonId={2}&view=scoringperiod&version=quick'

# years to iteratre through
years = [2017]
# weeks list to iterate through, max is 1 to 13
weeks = [1, 2, 3, 4, 5]
# id of team to start with
team_ID = 1
# list to store team objects
team_data = []

# loop through each team
for team in team_IDs:
    # create a team object
    temp_team = Team(team)
    # loop through each year
    for year in years:
        # loop through each week
        for week in weeks:
            # if week is less than 13, parse normally
            # 2013 will be parsed normally for week 13, while other years will skip
            if year == 2013 or (year > 2013 and week != 13):
                # get the url with formatting
                r = requests.get(base_url.format(team_ID, week, year))
                # use BeautifulSoup to get the webpage
                soup = BeautifulSoup(r.text, 'html.parser')
                # find the table with matchup data
                table = soup.find('table', class_='playerTableTable tableBody')
                # create a MatchStats object
                temp_match = MatchStats(team, year, week)
                # loop through players of one team's match (rows in the html table)
                for row in table.find_all('tr')[3:11]:
                    # get all matchup data (table data in html table)
                    line = row.find_all('td')
                    # 2016 matchups introduced new formatting
                    if year < 2016:
                        # if the first td has "Total" break the loop
                        if line[0].text == "Total":
                            break
                        else:
                            # split player name from other text
                            player_name, rhs = line[0].text.split(",", 1)
                            # get position
                            position = rhs[-2:]
                            # get players points
                            if line[1].text == '** BYE **':
                                points = line[2].text
                            else:
                                points = line[3].text
                            temp_match.add_data(position, points, player_name)
                    # otherwise extract the data
                    else:
                        # position of the player is first td
                        position = line[0].text
                        # if the position is FLEX, determine the actual position
                        # known bug if injury
                        if position == 'FLEX':
                            position = line[1].text[-2:]
                            if 'O' in position or 'Q' in position or 'D' in position:
                                position = line[1].text[-5:-3]
                            elif position=='IR':
                                position = line[1].text[-6:-4]
                            else:
                                pass

                        # boolean to determine if an error is raised or not
                        err_raise = False
                        try:
                            # try to extract player name
                            player_name = line[1].find('a').text
                        # this error gets raised if there is a blank roster spot
                        except AttributeError:
                            # set player_name to n/a, and mark error raised boolean as true
                            player_name = 'n/a'
                            err_raise = True
                        # boolean to determine if bye week player was played
                        bye_week_player = False
                        # if an error was raised, then points = 0
                        if err_raise:
                            points = 0
                        # if a player on bye was played
                        elif line[2].text == '** BYE **':
                            # set boolean to true
                            bye_week_player = True
                            points = 0
                        # otherwise points is extracted from table row
                        else:
                            points = line[4].text
                        # add the data to the match unless it is a bye week player
                        if not bye_week_player:
                            # print("{}|{}|{}|{}".format(team, position, player_name, points))
                            temp_match.add_data(position, points, player_name)
                # add the full match to the team match list
                temp_team.add_match(temp_match)
    # go to next team
    team_ID += 1
    # add team object to the team_data list
    team_data.append(temp_team)

# header for csv file
out_file_header = ['YEAR', 'WEEK', 'TEAM_NAME', 'QB_NAME', 'QB_SCORE',
            'RB_NAME', 'RB_SCORE','RB_NAME', 'RB_SCORE','WR_NAME',
            'WR_SCORE', 'WR_NAME', 'WR_SCORE', 'TE_NAME', 'TE_SCORE',
            'DST_NAME', 'DST_SCORE','FLEX_NAME','FLEX_POS', 'FLEX_SCORE']

# loop through each team object
for team in team_data:
    # make name of csv file the name of the player .csv
    out_name = team.teamName + '.csv'
    # open the csv file
    with open(out_name, 'w', newline='') as out:
        # create a csv writer
        csv_out = csv.writer(out)
        # write the header to the csv file
        csv_out.writerow(out_file_header)
        # loop through each match
        for match in team.Matches:
            # line is used to get the data in the correct order
            line = [match.year, match.week, match.team]

            # for each position, try to get the data from the match object
            # if an error is raised, set that player to n/a and points to 0

            # add qb
            try:
                line.append(match.qb[0])
                line.append(match.qb[1])
            except IndexError:
                line.append('n/a')
                line.append(0)

            # add rb1
            try:
                line.append(match.rb[0][0])
                line.append(match.rb[0][1])
            except IndexError:
                line.append('n/a')
                line.append(0)
            # add rb2
            try:
                line.append(match.rb[1][0])
                line.append(match.rb[1][1])
            except IndexError:
                line.append('n/a')
                line.append(0)

            # add wr1
            try:
                line.append(match.wr[0][0])
                line.append(match.wr[0][1])
            except IndexError:
                line.append('n/a')
                line.append(0)
            # add wr2
            try:
                line.append(match.wr[1][0])
                line.append(match.wr[1][1])
            except IndexError:
                line.append('n/a')
                line.append(0)

            # add tight end
            try:
                line.append(match.te[0][0])
                line.append(match.te[0][1])
            except IndexError:
                line.append('n/a')
                line.append(0)

            # add defense
            try:
                line.append(match.dst[0])
                line.append(match.dst[1])
            except IndexError:
                line.append('n/a')
                line.append(0)

            # add the flex
            try:  # try the rb first
                line.append(match.rb[2][0])
                line.append('rb')
                line.append(match.rb[2][1])
            except IndexError:
                try:  # if error, try the wr
                    line.append(match.wr[2][0])
                    line.append('wr')
                    line.append(match.wr[2][1])
                except IndexError:
                    try:  # if error try te
                        line.append(match.te[1][0])
                        line.append('te')
                        line.append(match.te[1][1])
                    except IndexError: # if error, null
                        line.append('n/a')
                        line.append('n/a')
                        line.append(0)
            # write the line to the csv file
            csv_out.writerow(line)
