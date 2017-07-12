import pandas as pd

path_matchup_player = r'C:\Users\estryshak\Desktop\FantasyFootball\RAW_DATA\CSV\All_Team_Matchups.csv'
path_matchup_results = r'C:\Users\estryshak\Desktop\FantasyFootball\RAW_DATA\CSV\Matchup_Results.csv'
path_standings = r'C:\Users\estryshak\Desktop\FantasyFootball\RAW_DATA\CSV\Standings.csv'

df_in = pd.read_csv(path_matchup_player, header=0)
df_player_stats = pd.DataFrame(df_in)  # contains all player stats

df_in = pd.read_csv(path_matchup_results, header=0)
df_results = pd.DataFrame(df_in)  # contains the matchup results

df_in = pd.read_csv(path_standings, header=0)
df_standings = pd.DataFrame(df_in)  # contains standings for each year



