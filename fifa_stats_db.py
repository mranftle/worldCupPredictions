import pandas as pd
import numpy as np
import random
import string,os, re, math
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import yaml
printable = set(string.printable)
fifa_dataset = pd.read_csv("data/fifa-18-demo-player-dataset/CompleteDataset.csv")
# player_attribute_data = pd.read_csv("data/fifa-18-demo-player-dataset/PlayerAttributeData.csv")
# player_personal_data = pd.read_csv("data/fifa-18-demo-player-dataset/PlayerPersonalData.csv")
# player_playing_position_data = pd.read_csv("data/fifa-18-demo-player-dataset/PlayerPlayingPositionData.csv")
name_nationality = pd.concat([fifa_dataset['Name'],fifa_dataset['Nationality'], fifa_dataset['Overall']], axis=1)


def clean_names(name):
    return re.sub('[^0-9a-zA-Z]+', '-', name.split()[-1]).lower().title()

def get_player_rating(country,roster):
    # print country
    # if country == 'Argentina':
    fifa_players = name_nationality.loc[name_nationality['Nationality'] == country]
    fifa_players['Name'] = fifa_players['Name'].map(lambda x: clean_names(x))
    # print fifa_players['Name']

    # print roster
    roster = map(clean_names, roster)
    # print fifa_players['Name']


    # print fifa_players.loc[fifa_players['Name'].isin()]
    players_with_ranks = pd.DataFrame(columns=['Name', 'Nationality', 'Overall'])
    for name in roster:
        # print name
        p = fifa_players.loc[fifa_players['Name'] == name]
        if not p.empty:
            # print type(p)
            players_with_ranks = players_with_ranks.append(p)
    return players_with_ranks.groupby(['Name']).max()

def average_player_ratings():
    # get team rosters
    rosters = dict()
    for filename in os.listdir('data/player_data/'):
        with open('data/player_data/' + filename, 'r') as f:
            content = f.readlines()
        rosters[filename.split('.')[0]]=content[0].split('\r')

    rosters = {k: get_player_rating(k.title(),v) for k,v in rosters.items()}

    print rosters
    # plot_with_plotly(rosters)


        # '''read in yml configs'''
        # with open('plotly_config.yaml', 'r') as f:
        #     doc = yaml.load(f)
        # username = doc['username']
        # password = doc['password']
        # py.sign_in(username, password)

        # average_player_rating = max_player_ratings['Overall'].mean()
        # if math.isnan(average_player_rating):
        #     average_player_rating = 0
        # average_player_ratings[country] = average_player_rating

    # for key, value in sorted(average_player_ratings.iteritems(), key=lambda (k,v): (v,k)):
    #     print "%s: %s" % (key, value)
    #
    # plot_with_plotly(average_player_ratings)

# def plot_with_plotly(roster):

    #     ratings = list(roster[team]['Overall'])
    #     temp_trace = go.Box(
    #         y = ratings,
    #         name = team.title()
    #     )
    #     traces.append(temp_trace)
    # py.iplot(traces)


    # N = len(roster)
    # c = ['hsl(' + str(h) + ',50%' + ',50%)' for h in np.linspace(0, 360, N)]
    #
    # data = [{
    #     'y':
    # }]

def main():
    average_player_ratings()

if __name__ == '__main__':
    main()

