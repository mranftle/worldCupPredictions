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
        if len(games_df[game[0]][game[1]]) == 0 and len(games_df[game[1]][game[0]]) == 0:
            if len(game[2]) == 0:
                game[2] = '0-0'
                games_df[game[0]][game[1]] = [(game[2],game[3])]
            elif int(game[2][0]) > int(game[2][2]):
                games_df[game[0]][game[1]] = [(game[2], game[3])]
                games_df[game[1]][game[0]] = [(game[2][2]+'-'+game[2][0], game[3])]
            else:
                games_df[game[0]][game[1]] = [(game[2][2]+'-'+game[2][0], game[3])]
        else:
            if len(game[2]) == 0:
                game[2] = '0-0'
                games_df[game[0]][game[1]] = games_df[game[0]][game[1]] + [(game[2],game[3])]
            elif int(game[2][0]) > int(game[2][2]):
                games_df[game[0]][game[1]]= games_df[game[0]][game[1]] + [(game[2], game[3])]
                games_df[game[1]][game[0]] = games_df[game[1]][game[0]] + [(game[2][2] + '-' + game[2][0], game[3])]

            else:
                games_df[game[0]][game[1]] = games_df[game[1]][game[0]] + [(game[2], game[3])]
                games_df[game[0]][game[1]] = games_df[game[0]][game[1]] + [(game[2][2] + '-' + game[2][0], game[3])]
    return games_df

def team_history(matchups):
    team_history = dict()
    for team in matchups:
        team_history[team] = {}
        for opp in matchups[team].iteritems():
            # print team, opp
            for match in opp[1]:
                if int(match[0][0]) > int(match[0][2]):
                    win = 1
                    tie = 0
                    lose = 0
                elif int(match[0][0]) < int(match[0][2]):
                    win = 0
                    tie = 0
                    lose = 1
                else:
                    win = 0
                    tie = 1
                    lose = 0
                if match[1] not in team_history[team]:
                    team_history[team][match[1]] = {"win": win, "lose": lose, "tie": tie, "goals_scored":int(match[0][0]), "goals_allowed":int(match[0][2]), "win_diff":int(match[0][0])-int(match[0][2])}
                else:
                    year_data_temp = team_history[team][match[1]]
                    team_history[team][match[1]]['win'] = team_history[team][match[1]]['win'] + win
                    team_history[team][match[1]]['lose'] = team_history[team][match[1]]['lose'] + lose
                    team_history[team][match[1]]['tie'] = team_history[team][match[1]]['tie'] + tie
                    team_history[team][match[1]]['goals_scored'] = team_history[team][match[1]]['goals_scored'] + int(match[0][0])
                    team_history[team][match[1]]['goals_allowed'] = team_history[team][match[1]]['goals_allowed'] + int(match[0][2])
                    team_history[team][match[1]]['win_diff'] = team_history[team][match[1]]['win_diff'] + int(match[0][0])-int(match[0][2])

    return team_history

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
            year = path.split('/')[3][:4]
            with open(path, 'r') as f:
                for line in f:

                    # clean data and get team1, team2 and scores
                    if not line in ['\n', '\r\n']:
                        scores = re.findall(r'[[0-9]-[0-9]', line)
                        if scores:
                            scores = scores[0]
                        #     # rearrage score so winner is always first
                        #     if int(scores[0]) < int(scores[2]):
                        #         scores = scores[2] + '-' +scores[0]

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
                            games.append([team1, team2, scores, year])

# print games
matchups = make_data_frame(games)
print team_history(matchups)
# print matchups['Hungary']['Bulgaria']
# print matchups['Bulgaria']['Hungary']
# matchups.to_csv('data/test_matchups.csv')

# statistics to get

# for each team: goals scored, goals allowed, wins, loses, win difference, per year
# for each year: total num goals, goal differential,
