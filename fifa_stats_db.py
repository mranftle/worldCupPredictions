import pandas as pd

fifa_dataset = pd.read_csv("data/fifa-18-demo-player-dataset/CompleteDataset.csv")
player_attribute_data = pd.read_csv("data/fifa-18-demo-player-dataset/PlayerAttributeData.csv")
player_personal_data = pd.read_csv("data/fifa-18-demo-player-dataset/PlayerPersonalData.csv")
player_playing_position_data = pd.read_csv("data/fifa-18-demo-player-dataset/PlayerPlayingPositionData.csv")
print fifa_dataset
