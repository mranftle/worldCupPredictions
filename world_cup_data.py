import os, re
import pandas as pd

# Get World Cup Rosters 
world_cup_rosters = pd.DataFrame(columns=['Year', 'Country', 'Players'])
for root, dirs, files in os.walk('data/world-cup/past_data', topdown=False):
    for name in files:
        path = os.path.join(root, name)
        if 'squads' in path:
            year = path.split('/')[3]
            country = path.split('/')[-1][:2]
            players = []
            with open(path, 'r') as f:
                for line in f:
                    if 'MF' in line or 'DF' in line or 'GK' in line:
                        player = line.split('#')[0]
                        players.append(" ".join(player.split()[2:]))

            world_cup_rosters = world_cup_rosters.append({'Year':year, 'Country':country, 'Players':players}, ignore_index=True)

print world_cup_rosters
