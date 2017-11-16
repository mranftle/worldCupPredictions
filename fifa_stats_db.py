import pandas as pd
import string
import os, re
printable = set(string.printable)
fifa_dataset = pd.read_csv("data/fifa-18-demo-player-dataset/CompleteDataset.csv")
# player_attribute_data = pd.read_csv("data/fifa-18-demo-player-dataset/PlayerAttributeData.csv")
# player_personal_data = pd.read_csv("data/fifa-18-demo-player-dataset/PlayerPersonalData.csv")
# player_playing_position_data = pd.read_csv("data/fifa-18-demo-player-dataset/PlayerPlayingPositionData.csv")
name_nationality = pd.concat([fifa_dataset['Name'],fifa_dataset['Nationality'], fifa_dataset['Overall']], axis=1)
# print  name_nationality

def isEnglish(s):
    return s.translate(None, string.punctuation).isalnum()


def clean_names(name):
    name = re.sub('[^0-9a-zA-Z]+', '*', name.lower().split()[-1].title())
    print name
    return name
    # return filter(lambda x: x in printable, name).split()[-1]

def get_player_rating(country,roster):
    # print country
    if country == 'Argentina':
        fifa_players = name_nationality.loc[name_nationality['Nationality'] == country]
        fifa_players['Name'] = fifa_players['Name'].map(lambda x: clean_names(x))
        # print fifa_players['Name']

        print roster
        name = map(clean_names, roster)
        print name
        print fifa_players['Name']


        # print fifa_players.loc[fifa_players['Name'].isin()]
                # print fifa_players.loc[fifa_players['Name'] == name]



# get team rosters
rosters = dict()
for filename in os.listdir('data/player_data/'):
    with open('data/player_data/' + filename, 'r') as f:
        content = f.readlines()

    # content = [x.strip('\r') for x in content]

    # content = content.split('\r')
    # print content
    rosters[filename.split('.')[0]]=content[0].split('\r')

# for key in rosters:
#     for player in rosters[key]:
#         # if player in fifa_dataset['Name']:
#         player_split = player.split()
#         # print player_split

rosters = {k: get_player_rating(k.title(),v) for k,v in rosters.items()}
