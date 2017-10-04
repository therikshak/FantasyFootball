import pandas as pd
import glob
import os

path = r'C:\Users\Rik\Desktop\FantasyFootball\RAW_DATA\CSV\By Team'
allFiles = glob.glob(os.path.join(path, "*.csv"))

dfFromEachFile = (pd.read_csv(f, header=0) for f in allFiles)
dfCat = pd.concat(dfFromEachFile, ignore_index=True)
df = pd.DataFrame(dfCat)

df.to_csv('All_Team_Matchups.csv', index=False)
