import os, re, math
import pandas as pd

# match_info_re_1 = re.compile(r'(\S+\s+|^)(\S+\s+|)[0-9]-[0-9](\s+\S+|)(\s+\S+|$)')
# match_info_re_2 = re.compile(r'(\S+\s+|^)(\S+\s+|)[0-9]-[0-9](\S+\s+|)(\s+\S+|)(\s+\S+|$)')
# match_info_re_3 = re.compile(r'(\S+\s+|^)(\S+\s+|)[0-9]-[0-9](\S+\s+|)(\S+\s+|)(\s+\S+|)(\s+\S+|$)')

world_cup_rosters = pd.DataFrame(columns=['Year', 'Country', 'Players'])
world_cup_matches = pd.DataFrame(columns=['Year', 'Round','Team1', 'Team2', 'Score1', 'Score2'])
PAST_CUP_DATA = 'data/world-cup/past_data'

games = []

def make_data_frame(games):
    # initialize dataframe
    game_set = set([game[0] for game in games] + [game[1] for game in games])
    games_df = pd.DataFrame(index=game_set)
    for game in game_set:
        games_df[game] = [[] for _ in range(len(game_set))]

    # add game data to dataframe
    for game in games:
        print games_df[game[0]][game[1]]
        if len(games_df[game[0]][game[1]]) == 0 and len(games_df[game[1]][game[0]]) == 0:
            games_df[game[0]][game[1]] = list(game[2])
            games_df[game[1]][game[0]] = list(game[2])
        else:
            games_df[game[0]][game[1]] = games_df[game[0]][game[1]] + list(game[2])
            games_df[game[1]][game[0]] = games_df[game[1]][game[0]] + list(game[2])

    return games_df


for root, dirs, files in os.walk(PAST_CUP_DATA, topdown=False):
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

        elif name == 'cup.txt' or name == 'cup_final.txt':
            year = path.split('/')[3]
            with open(path, 'r') as f:
                for line in f:

                    # clean data and get team1, team2 and scores
                    if not line in ['\n', '\r\n']:
                        scores = re.findall(r'[[0-9]-[0-9]', line)
                        if '@' in line:
                            temp = re.findall(r'([A-Z]\w+)', line.split('@')[0])[1:]
                            if temp[0] == str('Jun'):
                                temp = temp[1:]
                            if len(temp) == 2:
                                team1 = temp[0]
                                team2 = temp[1]
                            elif len(temp) == 4:
                                if temp[3] == str('Emirates'):
                                    team1 = temp[0]
                                    team2 = '-'.join(temp[1:])
                                elif temp[2] == str('Emirates'):
                                    team1 = '-'.join(temp[:3])
                                    team2 = temp[3]
                                else:
                                    team1 = '-'.join(temp[:2])
                                    team2 = '-'.join(temp[2:])
                            elif len(temp) == 5:
                                team1 = '-'.join(temp[:2])
                                team2= '-'.join(temp[2:])
                            elif temp[0] == str('United') \
                                    or temp[0] == str('South') \
                                    or temp[0] == str('Bosnia') \
                                    or temp[0] == str('Costa') \
                                    or temp[0] == str('North') \
                                    or temp[0] == str('New') \
                                    or temp[0] == str('East') \
                                    or temp[0] == str('Trinidad') \
                                    or temp[0] == str('Saudi') \
                                    or temp[0] == str('West') \
                                    or temp[0] == str('Northern') \
                                    or temp[0] == str('Soviet') \
                                    :
                                team1 = '-'.join(temp[:2])
                                team2 = temp[2]
                            else:
                                team1 = temp[0]
                                team2 = '-'.join(temp[1:])

                            games.append([team1, team2, scores])

matchups = make_data_frame(games)

# get statistics
for team in matchups:
    for opp in matchups[team].iteritems():
        print opp



# put game data into dataframe
