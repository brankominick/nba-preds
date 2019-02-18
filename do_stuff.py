import pandas as pd
import numpy
import json
from pprint import pprint
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.linear_model import LogisticRegression

with open('data.json') as f:
  data = json.loads(f.read())



keys = []
frames = []


for game in data:
    for key, d in game.items():
        keys.append(key)
        frames.append(pd.DataFrame.from_dict(d, orient='index'))

game_df = pd.concat(frames, keys=keys, sort=True)
game_df.names = ['Game','Teams']
#print(game_df)



game_df.xs('Boston Celtics', level=1).index.values
