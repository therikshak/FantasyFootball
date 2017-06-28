from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests

# example URLS
# http://games.espn.com/ffl/boxscorequick?leagueId=416193&teamId=1&scoringPeriodId=1&seasonId=2013&view=scoringperiod&version=quick
# http://games.espn.com/ffl/boxscorequick?leagueId=416193&teamId=3&scoringPeriodId=1&seasonId=2013&view=scoringperiod&version=quick
# http://games.espn.com/ffl/boxscorequick?leagueId=416193&teamId=4&scoringPeriodId=1&seasonId=2013&view=scoringperiod&version=quick


#teamId by index for 2013
teamID2013 = ['Erik Stryshak', 'Charlie Frank', "Brendan Hart",
            'Stefan Hanish', 'Andrew McDowell', 'Horlacher',
            'Geoffrey Raclin', 'Trey Shmo', 'Joe Buelter',
            'Tommy Stupp', 'Peter Condie', 'James Carman',
            'Chris Dorr', 'Ozair Ferozuddin']
#teamId by index for other years
teamID = ['Erik Stryshak', 'Charlie Frank', "Brendan Hart",
            'Stefan Hanish', 'Andrew McDowell', 'Horlacher',
            'Geoffrey Raclin', 'Trey Shmo', 'Richard Graney',
            'Tommy Stupp', 'Peter Condie', 'James Carman',
            'Chandler Dalton', 'Ozair Ferozuddin']
#0 is teamId, add 1 for url
# 1 is week, 2013 had 13 weeks, every other season had 12
# 2 is year 2013-2016 for now
#easy option is to only extract left team data and go teamId 1-14 for each week and year
baseURL = 'http://games.espn.com/ffl/boxscorequick?leagueId=416193&teamId={0}&scoringPeriodId={1}&seasonId={2}&view=scoringperiod&version=quick'
