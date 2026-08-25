import numpy
import pandas as pd
import matplotlib.pyplot as plt

# Matches dataframes
df_matches_2020 = pd.read_csv("atp_matches_2020.csv")
df_matches_2021 = pd.read_csv("atp_matches_2021.csv")
df_matches_2022 = pd.read_csv("atp_matches_2022.csv")
df_matches_2023 = pd.read_csv("atp_matches_2023.csv")
df_matches_2024 = pd.read_csv("atp_matches_2024.csv")
df_matches_2025 = pd.read_csv("atp_matches_2025.csv")
df_matches_2026 = pd.read_csv("atp_matches_2026.csv")
matches_list = [df_matches_2020, df_matches_2021, df_matches_2022, df_matches_2023, df_matches_2024, df_matches_2025, df_matches_2026]
df_matches = pd.concat(matches_list, axis=0, ignore_index=True)

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

def name_to_player(player_name):
    first_name, last_name = player_name.split()
    player = df_players.loc[(df_players["name_first"] == first_name) & (df_players["name_last"] == last_name)]
    return player

def id_to_player(player_id):
    player = df_players.loc[df_players["player_id"] == player_id]
    return player


# How many matches are there
print(f"Number of matches: {len(df_matches)}")

# What columns exist
print(df_matches.columns)

# Which columns contain missing data
print(df_matches.info())

# How many matches occur on each surface
hard_matches = df_matches[df_matches.surface == "Hard"]
print(f"Number of matches on hard: {len(hard_matches)}")
clay_matches = df_matches[df_matches.surface == "Clay"]
print(f"Number of matches on clay: {len(clay_matches)}")
grass_matches = df_matches[df_matches.surface == "Grass"]
print(f"Number of matches on grass: {len(grass_matches)}")

# What tournaments exist
print(f"Number of unique tournaments: {df_matches['tourney_name'].nunique()}")
print(df_matches["tourney_name"].value_counts())

# How many unique players are there
print(f"Number of unique players: {df_players['player_id'].nunique()}")

# What percentage of matches are won by the higher-ranked player
def find_higher_rank_win_percentage(matches: pd.DataFrame):
    total_count = 0
    winner_count = 0
    for index, match in matches.iterrows():
        winner_rank = match['winner_rank']
        loser_rank = match['loser_rank']
        # compute if no ranks are missing (excludes unranked players)
        if pd.notna(winner_rank) and pd.notna(loser_rank):
            if winner_rank < loser_rank:
                winner_count += 1

            total_count += 1

    return (winner_count / total_count) * 100

print(f"Percentage of higher ranked winner: {find_higher_rank_win_percentage(df_matches)}")

# Does that percentage differ between hard/clay/grass
print(f"Percentage of higher ranked winner hard: {find_higher_rank_win_percentage(hard_matches)}")
print(f"Percentage of higher ranked winner clay: {find_higher_rank_win_percentage(clay_matches)}")
print(f"Percentage of higher ranked winner grass: {find_higher_rank_win_percentage(grass_matches)}")

# How does ranking difference relate to probability of winning
df_matches["rank_diff"] = (df_matches["winner_rank"] - df_matches["loser_rank"]).abs()
df_matches["higher_ranked_won"] = df_matches["winner_rank"] < df_matches["loser_rank"]

bins = [0, 10, 20, 30, 50, 100, 200, 500]
mid = [5, 15, 25, 40, 75, 150, 350]
widths = [10, 10, 10, 20, 50, 100, 300]
colors = ["red", "orange", "yellow", "green", "blue", "purple", "pink"]
df_matches["rank_bucket"] = pd.cut(df_matches["rank_diff"], bins=bins)

df = df_matches.groupby("rank_bucket")["higher_ranked_won"].mean()
print(df)

plt.bar(mid, df, width=widths, color=colors)
plt.show()

# Which players have played the most matches
wins_per_id = df_matches["winner_id"].value_counts()
loss_per_id = df_matches["loser_id"].value_counts()
unique_winner_ids = df_matches["winner_id"].unique()
unique_loser_ids = df_matches["loser_id"].unique()
unique_player_ids = numpy.unique(numpy.concatenate((unique_winner_ids, unique_loser_ids)))
total_matches_list = []
win_percent_list = []
unique_player_names = [id_to_player(id).iloc[0]["name_first"] + " " + id_to_player(id).iloc[0]["name_last"] for id in unique_player_ids]
for id in unique_player_ids:
    try:
        win_count = wins_per_id[id]
    except:
        # no wins
        win_count = 0
    try:
        lose_count = loss_per_id[id]
    except:
        #no losses
        lose_count = 0
    total_matches = win_count + lose_count

    total_matches_list.append(total_matches)
    win_percent_list.append((win_count/total_matches) * 100)

data = {
    "player_id": unique_player_ids,
    "player_name": unique_player_names,
    "match_count": total_matches_list,
    "win_percent": win_percent_list
}

df_match_count_per_id = pd.DataFrame(data)
print(df_match_count_per_id.sort_values("match_count", ascending=False))
