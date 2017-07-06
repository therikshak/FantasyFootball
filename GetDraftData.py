from bs4 import BeautifulSoup
import requests
from MatchStats import MatchStats
from Team import Team
import csv

baseURL = "http://games.espn.com/ffl/tools/draftrecap?leagueId=416193&seasonId={0}&mode=1"

years = [2013, 2014, 2015, 2016]

# list to store team objects
teamData = []