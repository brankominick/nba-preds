import pandas as pd
import numpy
import json
from pprint import pprint
#from sklearn.model_selection import cross_val_score
#from sklearn.model_selection import KFold
#from sklearn.linear_model import LogisticRegression

with open('data.json') as f:
  data = json.loads(f.read())



keys = []
frames = []

#no longer works; i may have messed up the data
"""for game in data:
    for key, d in game.items():
        keys.append(key)
        frames.append(pd.DataFrame.from_dict(d, orient='index'))

game_df = pd.concat(frames, keys=keys, sort=True)
game_df.names = ['Game','Teams']"""
#print(game_df)


reform = [{(outerKey, innerKey): values for outerKey, innerDict in game.items() for innerKey, values in innerDict.items()} for game in data]
#pprint(reform)
#games = pd.MultiIndex.from_tuples(reform).to_frame()
dfs=[]
for i in reform:
    dfs.append((pd.DataFrame(i)).T)
#games = pd.DataFrame.from_records(reform)
game_df = pd.DataFrame()
for i in dfs:
    game_df= game_df.append(i)
#print(game_df)

boston_games = game_df.xs('Boston Celtics', level=1).index.values

print(game_df.loc[boston_games[0]])
