import os, re
import pandas as pd

match_info_re_1 = re.compile(r'(\S+\s+|^)(\S+\s+|)[0-9]-[0-9](\s+\S+|)(\s+\S+|$)')
match_info_re_2 = re.compile(r'(\S+\s+|^)(\S+\s+|)[0-9]-[0-9](\S+\s+|)(\s+\S+|)(\s+\S+|$)')
match_info_re_3 = re.compile(r'(\S+\s+|^)(\S+\s+|)[0-9]-[0-9](\S+\s+|)(\S+\s+|)(\s+\S+|)(\s+\S+|$)')

world_cup_rosters = pd.DataFrame(columns=['Year', 'Country', 'Players'])
world_cup_matches = pd.DataFrame(columns=['Year', 'Round','Team1', 'Team2', 'Score1', 'Score2'])

# Get World Cup Rosters and Match Outcomes
i = 0
for root, dirs, files in os.walk('data/world-cup/past_data', topdown=False):
    for name in files:
        path = os.path.join(root, name)
        if 'squads' in path:
            # yah yah
            continue
            # year = path.split('/')[3]
            # country = path.split('/')[-1][:2]
            # players = []
            # with open(path, 'r') as f:
            #     for line in f:
            #         if 'MF' in line or 'DF' in line or 'GK' in line:
            #             player = line.split('#')[0]
            #             players.append(" ".join(player.split()[2:]))
            #
            # world_cup_rosters = world_cup_rosters.append({'Year':year, 'Country':country, 'Players':players}, ignore_index=True)
        elif name == 'cup.txt' or name == 'cup_final.txt':
            year = path.split('/')[3]
            # print year
            with open(path, 'r') as f:
                for line in f:
                    # continue
                    if not line in ['\n', '\r\n']:
                        # print line
                        # if not '@' in line:
                        #     continue
                        #     # print line
                        # else:
                        scores = re.findall(r'[[0-9]-[0-9]', line)
                        print scores
                        # if len(scores) == 1:
                        #     info = re.findall(match_info_re_1, line)
                        # elif len(scores) == 2:
                        #     info = re.findall(match_info_re_2, line)
                        # elif len(scores)==3:
                        #     info = re.findall(match_info_re_3, line)
                        # else:
                        #     info =[]
                        #     # print line
                        # print info
                        # if len(info)>0:
                        #     teams = []
                        #     for x in info[0]:
                        #         if re.match(team_name_re, x):
                        #             teams.append(x)
                        #     print teams

         # else if cup_finals.txt
        #else if quali ** only for 2014
            # print path
# print i
# print world_cup_matches
