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
df_matches["tourney_date"] = pd.to_datetime(df_matches["tourney_date"], format="%Y%m%d")

# Players dataframe
df_players = pd.read_csv("atp_players.csv")
#df_players["dob"] = pd.to_datetime(df_players["dob"], format="%Y%m%d")


df_current_rankings = pd.read_csv("atp_rankings_current.csv")
df_rankings_20s = pd.read_csv("atp_rankings_20s.csv")
rankings_list = [df_current_rankings, df_rankings_20s]
# combine dataframes to get all the rankings
df_rankings = pd.concat(rankings_list, axis=0, ignore_index=True)

# convert date int to datetime
df_rankings['ranking_date'] = pd.to_datetime(df_rankings['ranking_date'], format='%Y%m%d')

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
#print(f"Number of matches: {len(df_matches)}")

# What columns exist
#print(df_matches.columns)

# Which columns contain missing data
#print(df_matches.info())

# How many matches occur on each surface
hard_matches = df_matches[df_matches.surface == "Hard"]
#print(f"Number of matches on hard: {len(hard_matches)}")
clay_matches = df_matches[df_matches.surface == "Clay"]
#print(f"Number of matches on clay: {len(clay_matches)}")
grass_matches = df_matches[df_matches.surface == "Grass"]
#print(f"Number of matches on grass: {len(grass_matches)}")

# What tournaments exist
#print(f"Number of unique tournaments: {df_matches['tourney_name'].nunique()}")
#print(df_matches["tourney_name"].value_counts())

# How many unique players are there
#print(f"Number of unique players: {df_players['player_id'].nunique()}")

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

#print(f"Percentage of higher ranked winner: {find_higher_rank_win_percentage(df_matches)}")

# Does that percentage differ between hard/clay/grass
#print(f"Percentage of higher ranked winner hard: {find_higher_rank_win_percentage(hard_matches)}")
#print(f"Percentage of higher ranked winner clay: {find_higher_rank_win_percentage(clay_matches)}")
#print(f"Percentage of higher ranked winner grass: {find_higher_rank_win_percentage(grass_matches)}")

# How does ranking difference relate to probability of winning
df_matches["rank_diff"] = (df_matches["winner_rank"] - df_matches["loser_rank"]).abs()
df_matches["higher_ranked_won"] = df_matches["winner_rank"] < df_matches["loser_rank"]

bins = [0, 10, 20, 30, 50, 100, 200, 500]
mid = [5, 15, 25, 40, 75, 150, 350]
widths = [10, 10, 10, 20, 50, 100, 300]
colors = ["red", "orange", "yellow", "green", "blue", "purple", "pink"]
df_matches["rank_bucket"] = pd.cut(df_matches["rank_diff"], bins=bins)

df = df_matches.groupby("rank_bucket")["higher_ranked_won"].mean()
#print(df)

plt.bar(mid, df, width=widths, color=colors)
plt.ylim(0, 1)
#plt.show()

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
#print(df_match_count_per_id.sort_values("match_count", ascending=False))

# Jannik Sinner: 206173

# Find a player's ranking
name = "Jannik Sinner"
id = name_to_player(name).iloc[0]["player_id"]
current_ranking = find_player_rankings(id).sort_values("ranking_date", ascending=False).iloc[0]["rank"]
print(f"Current Ranking: {current_ranking}")

# Find a player's ranking at a given date
date = pd.Timestamp("2021-07-01")
rankings = find_player_rankings(id).sort_values("ranking_date", ascending=False)
rankings_upto_date = rankings[rankings["ranking_date"] <= date]
ranking_at_date = rankings_upto_date.iloc[0]["rank"]
print(f"Ranking on {date.strftime('%Y-%m-%d')}: {ranking_at_date}")

# Find a player's previous matches before a given date
df_matches = df_matches.sort_values("tourney_date", ascending=False)
previous_matches = df_matches[
    (
        (df_matches["winner_name"] == name) |
        (df_matches["loser_name"] == name)
    )
    &
    (df_matches["tourney_date"] < date)
]
print(f"Previous mathces upto {date.strftime('%Y-%m-%d')}: {previous_matches}")

last_10 = previous_matches.head(10)
last_5 = previous_matches.head(5)

# Calculate a player's career win percentage before a given date
previous_won_matches = df_matches[(df_matches["winner_name"] == name) & (df_matches["tourney_date"] < date)]
print(f"Win percentage before {date.strftime('%Y-%m-%d')}: {(len(previous_won_matches) / len(previous_matches))*100}%")

# Calculate win percentage over their last 5 matches
won_last_5 = last_5[last_5["winner_name"] == name]
print(f"Win percentage of last 5 matches: {(len(won_last_5) / len(last_5))*100}%")

# Calculate win percentage over their last 10 matches
won_last_10 = last_10[last_10["winner_name"] == name]
print(f"Win percentage of last 10 matches: {(len(won_last_10) / len(last_10))*100}%")

# Calculate win percentage on hard / clay / grass

# Calculate recent win percentage on a particular surface

# Find number of days since player's previous match

# Compare head-to-head between two players

# Compare head-to-head before a given date

# Compare head-to-head on a particular surface

# Calculate average opponent ranking over recent matches

# Calculate percentage of matches where the higher-ranked player wins

# Calculate a player's win percentage against higher-ranked opponents

# Calculate a player's win percentage against lower-ranked opponents

# Build a function that takes two players + a date and returns all of the above

# Build your first Elo rating system

# Build separate hard / clay / grass Elo ratings

# Turn each historical match into a row of pre-match features

# Build a very simple prediction baseline
