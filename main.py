import numpy
import pandas as pd
import matplotlib

# Players dataframe
df_players = pd.read_csv("atp_players.csv")
df_players["dob"] = pd.to_datetime(df_players["dob"], format='mixed')


df_current_rankings = pd.read_csv("atp_rankings_current.csv")
df_rankings_20s = pd.read_csv("atp_rankings_20s.csv")
rankings_list = [df_current_rankings, df_rankings_20s]
# combine dataframes to get all the rankings
df_rankings = pd.concat(rankings_list, axis=0, ignore_index=True)

# convert date int to datetime
df_rankings['ranking_date'] = pd.to_datetime(df_rankings['ranking_date'], format='mixed')

first_names = df_players["name_first"]
last_names = df_players["name_last"]

names = first_names + " " + last_names

def find_player_rankings(player_id):
    return df_rankings.loc[df_rankings["player"] == player_id]

def name_to_id(player_name):
    names = player_name.split()
    df_players.groupby()

#test commit
