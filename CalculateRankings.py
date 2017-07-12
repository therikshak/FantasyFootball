import pandas as pd
import numpy as np

path_matchup_player = r'C:\Users\estryshak\Desktop\FantasyFootball\RAW_DATA\CSV\All_Team_Matchups.csv'
path_matchup_results = r'C:\Users\estryshak\Desktop\FantasyFootball\RAW_DATA\CSV\Matchup_Results.csv'
path_standings = r'C:\Users\estryshak\Desktop\FantasyFootball\RAW_DATA\CSV\Standings.csv'

df_in = pd.read_csv(path_matchup_player, header=0)
df_player_stats = pd.DataFrame(df_in)  # contains all player stats

df_in = pd.read_csv(path_matchup_results, header=0)
df_results = pd.DataFrame(df_in)  # contains the matchup results

df_in = pd.read_csv(path_standings, header=0)
df_standings = pd.DataFrame(df_in)  # contains standings for each year

new_columns = ['Team', 'Year', 'Total_Points', 'Average_Points', 'STD_Points', 'QB_Points', 'QB_STD', 'RB_Points',
               'RB_STD', 'WR_Points', 'WR_STD', 'TE_Points', 'TE_STD', 'DST_Points', 'DST_STD', 'FLEX_Points',
               'FLEX_STD', 'Made_Playoffs', 'Regular_Season_Finish', 'Wins']

df = pd.merge(df_player_stats, df_standings, on='TEAM_NAME')

df.to_csv('Merged.csv', index=False)
