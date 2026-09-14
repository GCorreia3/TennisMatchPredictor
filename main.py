import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
from math import *


# Matches dataframes
df_matches_2010 = pd.read_csv("2010.csv")
df_matches_2011 = pd.read_csv("2011.csv")
df_matches_2012 = pd.read_csv("2012.csv")
df_matches_2013 = pd.read_csv("2013.csv")
df_matches_2014 = pd.read_csv("2014.csv")
df_matches_2015 = pd.read_csv("2015.csv")
df_matches_2016 = pd.read_csv("2016.csv")
df_matches_2017 = pd.read_csv("2017.csv")
df_matches_2018 = pd.read_csv("2018.csv")
df_matches_2019 = pd.read_csv("2019.csv")
df_matches_2020 = pd.read_csv("2020.csv")
df_matches_2021 = pd.read_csv("2021.csv")
df_matches_2022 = pd.read_csv("2022.csv")
df_matches_2023 = pd.read_csv("2023.csv")
df_matches_2024 = pd.read_csv("2024.csv")
df_matches_2025 = pd.read_csv("2025.csv")
df_matches_2026 = pd.read_csv("2026.csv")
df_ongoing = pd.read_csv("ongoing_tourneys.csv")
matches_list = [
    df_matches_2010, df_matches_2011, df_matches_2012, df_matches_2013, df_matches_2014, df_matches_2015, df_matches_2016, df_matches_2017, df_matches_2018, df_matches_2019,
    df_matches_2020, df_matches_2021, df_matches_2022, df_matches_2023, df_matches_2024, df_matches_2025, df_matches_2026, df_ongoing
]
df_matches = pd.concat(matches_list, axis=0, ignore_index=True)
df_matches["tourney_date"] = pd.to_datetime(df_matches["tourney_date"], format="%Y%m%d")

# Players dataframe
df_players = pd.read_csv("ATP_Database.csv")
df_players["birthdate"] = pd.to_datetime(df_players["birthdate"], format="%Y%m%d")
df_players = df_players.drop(columns=["turnedpro", "birthplace", "coaches", "atpname"])
# columns: id, player, weight, height, hand, backhand, ioc

#print(df_players.info())

df_rankings_2010 = pd.read_csv("atp_rankings_2010.csv")
df_rankings_2011 = pd.read_csv("atp_rankings_2011.csv")
df_rankings_2012 = pd.read_csv("atp_rankings_2012.csv")
df_rankings_2013 = pd.read_csv("atp_rankings_2013.csv")
df_rankings_2014 = pd.read_csv("atp_rankings_2014.csv")
df_rankings_2015 = pd.read_csv("atp_rankings_2015.csv")
df_rankings_2016 = pd.read_csv("atp_rankings_2016.csv")
df_rankings_2017 = pd.read_csv("atp_rankings_2017.csv")
df_rankings_2018 = pd.read_csv("atp_rankings_2018.csv")
df_rankings_2019 = pd.read_csv("atp_rankings_2019.csv")
df_rankings_2020 = pd.read_csv("atp_rankings_2020.csv")
df_rankings_2021 = pd.read_csv("atp_rankings_2021.csv")
df_rankings_2022 = pd.read_csv("atp_rankings_2022.csv")
df_rankings_2023 = pd.read_csv("atp_rankings_2023.csv")
df_rankings_2024 = pd.read_csv("atp_rankings_2024.csv")
df_rankings_2025 = pd.read_csv("atp_rankings_2025.csv")
df_rankings_2026 = pd.read_csv("atp_rankings_2026.csv")
rankings_list = [
    df_rankings_2026, df_rankings_2025, df_rankings_2024, df_rankings_2023, df_rankings_2022, df_rankings_2021, df_rankings_2020,
    df_rankings_2019, df_rankings_2018, df_rankings_2017, df_rankings_2016, df_rankings_2015, df_rankings_2014, df_rankings_2013, df_rankings_2012, df_rankings_2011, df_rankings_2010
]
# combine dataframes to get all the rankings
df_rankings = pd.concat(rankings_list, axis=0, ignore_index=True)
# columns: ranking_date, rank, player, ranking_points

# convert date int to datetime
df_rankings['ranking_date'] = pd.to_datetime(df_rankings['ranking_date'], format='%Y%m%d')
#df_rankings = df_rankings.sort_values("ranking_date", ascending=True)

def find_player_rankings(player_name):
    return df_rankings.loc[df_rankings["player"] == player_name]

def name_to_player(player_name):
    player = df_players.loc[df_players["player"] == player_name]
    return player

def id_to_player(player_id):
    player = df_players.loc[df_players["id"] == player_id]
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
#print(f"Number of unique players: {df_players['id'].nunique()}")

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

    if total_count == 0:
        return 0
    else:
        return (winner_count / total_count) * 100

#print(f"Percentage of higher ranked winner: {find_higher_rank_win_percentage(df_matches)}%")

# Does that percentage differ between hard/clay/grass
#print(f"Percentage of higher ranked winner hard: {find_higher_rank_win_percentage(hard_matches)}%")
#print(f"Percentage of higher ranked winner clay: {find_higher_rank_win_percentage(clay_matches)}%")
#print(f"Percentage of higher ranked winner grass: {find_higher_rank_win_percentage(grass_matches)}%")

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

# probability of player with rank1 beating player with rank2 based off previous data
def win_probability_from_ranking(rank1, rank2):
    # check for nan ranking
    if pd.isna(rank1):
        rank1 = 2000

    if pd.isna(rank2):
        rank2 = 2000

    rank_diff = rank1 - rank2
    abs_rank_diff = abs(rank_diff)

    for index, x in enumerate(bins):
        if x == 0:
            continue
        if abs_rank_diff <= x:
            probability = df.iloc[index-1]
            break
        elif abs_rank_diff > 500:
            probability = df.iloc[6]

    if rank_diff > 0: # positive means rank1 is higher than 2
        probability = 1-probability

    return probability

# plt.plot(mid, df)
# plt.ylim(0, 1)
# plt.xlabel("Rank difference")
# plt.ylabel("Probability of highest rank winning")
# plt.title("Probability of highest rank winning vs ranking difference")
# plt.savefig("prob_rank_winning_vs_rank_dif2.png")
# plt.show()

# Which players have played the most matches
wins_per_id = df_matches["winner_id"].dropna().value_counts()
loss_per_id = df_matches["loser_id"].dropna().value_counts()
unique_winner_ids = df_matches["winner_id"].dropna().unique()
unique_loser_ids = df_matches["loser_id"].dropna().unique()
unique_player_ids = np.unique(np.concatenate((unique_winner_ids, unique_loser_ids)))
total_matches_list = []
win_percent_list = []
unique_player_names = [id_to_player(id).iloc[0]["player"] for id in unique_player_ids]
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
current_ranking = find_player_rankings(name).sort_values("ranking_date", ascending=False).iloc[0]["rank"]
#print(f"Current {name} Ranking: {current_ranking}")

date = pd.Timestamp("2025-06-26")

# Build a function that takes two players + a date and returns all of the above

def get_player_stats(df_matches, name, date, surface):
    info_dict = {}

    id = name_to_player(name).iloc[0]["id"]
    info_dict["player_id"] = id

    # Find a player's ranking at a given date
    rankings = find_player_rankings(name).sort_values("ranking_date", ascending=False)
    rankings_upto_date = rankings[rankings["ranking_date"] <= date]
    ranking_at_date = rankings_upto_date.iloc[0]["rank"]
    #print(f"Ranking on {date.strftime('%Y-%m-%d')}: {ranking_at_date}")

    info_dict["ranking"] = int(ranking_at_date)

    # Find a player's previous matches before a given date
    df_matches = df_matches.sort_values(["tourney_date", "match_num"], ascending=[False, False])
    previous_matches = df_matches[
        (
            (df_matches["winner_name"] == name) |
            (df_matches["loser_name"] == name)
        )
        &
        (df_matches["tourney_date"] < date)
    ]
    #print(f"Previous mathces upto {date.strftime('%Y-%m-%d')}: {previous_matches}")

    #info_dict["previous_matches"] = previous_matches

    last_10 = previous_matches.head(10)
    last_5 = previous_matches.head(5)

    # Calculate a player's career win percentage before a given date
    previous_won_matches = previous_matches[previous_matches["winner_name"] == name]
    #print(f"Win percentage before {date.strftime('%Y-%m-%d')}: {(len(previous_won_matches) / len(previous_matches))*100}%")

    # Calculate win percentage over their last 5 matches
    won_last_5 = last_5[last_5["winner_name"] == name]
    #print(f"Win percentage of last 5 matches: {(len(won_last_5) / len(last_5))*100}%")

    info_dict["last_5_win_rate"] = len(won_last_5) / len(last_5)

    # Calculate win percentage over their last 10 matches
    won_last_10 = last_10[last_10["winner_name"] == name]
    #print(f"Win percentage of last 10 matches: {(len(won_last_10) / len(last_10))*100}%")

    info_dict["last_10_win_rate"] = len(won_last_10) / len(last_10)

    # Calculate win percentage on surface
    player_surface_matches = previous_matches[previous_matches["surface"] == surface]
    player_won_surface_matches = player_surface_matches[player_surface_matches["winner_name"] == name]
    #print(f"Win percentage of hard for {name}: {(len(player_won_surface_matches)/len(player_surface_matches))*100}%")

    info_dict[f"{surface}_win_rate"] = len(player_won_surface_matches)/len(player_surface_matches)

    # Calculate recent win percentage on a particular surface
    last_10_surface = player_surface_matches.head(10)
    player_won_last_10_surface = last_10_surface[last_10_surface["winner_name"] == name]
    #print(f"Win percentage of last 10 matches on {surface} for {name}: {(len(player_won_last_10_surface)/len(last_10_surface))*100}%")

    # Find number of days since player's previous match
    last_match_date = previous_matches.head(1).iloc[0]["tourney_date"]
    days_since_last_match = (date - last_match_date).days
    #print(f"Number of days since last match: {days_since_last_match}")

    info_dict["days_since_last_match"] = days_since_last_match

    # Calculate a player's win percentage against higher-ranked opponents
    prev_matches_v_higher_rank = previous_matches[
            (previous_matches["winner_name"] == name) & (previous_matches["winner_rank"] > previous_matches["loser_rank"])
            |
            (previous_matches["loser_name"] == name) & (previous_matches["winner_rank"] < previous_matches["loser_rank"])
        ]

    #print(f"{name} win percentage vs higher ranked ops: {find_higher_rank_win_percentage(prev_matches_v_higher_rank)}%")

    info_dict["win_rate_v_higher_ops"] = find_higher_rank_win_percentage(prev_matches_v_higher_rank)/100

    # Calculate a player's win percentage against lower-ranked opponents
    prev_matches_v_lower_rank = previous_matches[
            (previous_matches["winner_name"] == name) & (previous_matches["winner_rank"] < previous_matches["loser_rank"])
            |
            (previous_matches["loser_name"] == name) & (previous_matches["winner_rank"] > previous_matches["loser_rank"])
        ]

    #print(f"{name} win percentage vs lower ranked ops: {find_higher_rank_win_percentage(prev_matches_v_lower_rank)}%")

    info_dict["win_rate_v_lower_ops"] = find_higher_rank_win_percentage(prev_matches_v_lower_rank)/100

    return pd.DataFrame([info_dict])

def find_upcoming_match_info(df_matches, name1, name2, date, surface):
    head_to_head_info = {}

    try:
        player1_info = get_player_stats(df_matches, name1, date, surface)
    except:
        return print("Player 1 Name doesn't exist")

    try:
        player2_info = get_player_stats(df_matches, name2, date, surface)
    except:
        return print("Player 2 Name doesn't exist")

    id1 = player1_info.iloc[0]["player_id"]
    id2 = player2_info.iloc[0]["player_id"]

    head_to_head_info["player_id1"] = id1
    head_to_head_info["player_id2"] = id2

    ranking1 = int(player1_info.iloc[0]["ranking"])
    ranking2 = int(player2_info.iloc[0]["ranking"])

    head_to_head_info["ranking1"] = ranking1
    head_to_head_info["ranking2"] = ranking2

    df_matches = df_matches.sort_values(["tourney_date", "match_num"], ascending=[False, False])
    previous_matches1 = df_matches[
        (
            (df_matches["winner_name"] == name1) |
            (df_matches["loser_name"] == name1)
        )
        &
        (df_matches["tourney_date"] < date)
    ]

    # Compare head-to-head before a given date
    previous_won_against = previous_matches1[previous_matches1["loser_name"] == name2]
    previous_lose_against = previous_matches1[previous_matches1["winner_name"] == name2]
    #print(f"{name1} vs {name2} (before {date.strftime('%Y-%m-%d')}): {len(previous_won_against)} vs {len(previous_lose_against)} wins")

    head_to_head_info["1vs2_wins"] = f"{len(previous_won_against)}:{len(previous_lose_against)}"

    # Compare head-to-head on a particular surface
    previous_won_against_grass = previous_won_against[previous_won_against["surface"] == "Grass"]
    previous_lose_against_grass = previous_lose_against[previous_lose_against["surface"] == "Grass"]
    #print(f"Grass h2h {name1} vs {name2} (before {date.strftime('%Y-%m-%d')}): {len(previous_won_against_grass)} vs {len(previous_lose_against_grass)} wins")

    head_to_head_info[f"1vs2_{surface}_wins"] = f"{len(previous_won_against_grass)}:{len(previous_lose_against_grass)}"

    # Calculate average opponent ranking over recent matches

    # Calculate percentage of matches where the higher-ranked player wins
    #print(f"Percent {name1} higher rank when beat {name2}: {find_higher_rank_win_percentage(previous_won_against)}%")
    head_to_head_info["win_rate_1_higher_rank"] = find_higher_rank_win_percentage(previous_won_against) / 100
    #print(f"Percent {name2} higher rank when beat {name1}: {find_higher_rank_win_percentage(previous_lose_against)}%")
    head_to_head_info["win_rate_2_higher_rank"] = find_higher_rank_win_percentage(previous_lose_against) / 100

    return head_to_head_info

#print(get_player_stats(df_matches, name, date, "Hard"))

# Predict who wins between two players based on who has a higher rank at the time

info = find_upcoming_match_info(df_matches, "Taylor Fritz", "Novak Djokovic", date, "Grass")
#print(info)
# if info["ranking1"] < info["ranking2"]:
#     print("Player 1 wins")
# else:
#     print("Player 2 wins")

# Build first Elo rating system

def get_expected_win_probability(elo1, elo2):
    return 1 / (1 + 10**((elo2-elo1)/400))

def update_elo(elo, win, probability):
    K = 32
    return elo + K * (win - probability)

def update_players_elo(elo1, elo2, win):
    probability = get_expected_win_probability(elo1, elo2)
    return update_elo(elo1, win, probability), update_elo(elo2, 1-win, 1-probability)

# Calculate Log_loss
def log_loss(win_outcome, win_probability):
    return -(win_outcome * log(win_probability) + (1 - win_outcome) * log(1 - win_probability))

df_matches = df_matches.sort_values(["tourney_date", "match_num"], ascending=[True, True]) # sort so first match in list is first dated match
df_matches = df_matches.dropna(subset=["surface"])
players_elo = {
    "Overall": {},
    "Hard": {},
    "Clay": {},
    "Grass": {},
    "Carpet": {}
}
elo_dates_history = []
elo_players_history = []
elo_history = []
surface_history = []
surface_elo_history = []
correct_guesses = 0
wrong_guesses = 0
surface_correct_guesses = 0
surface_wrong_guesses = 0
random_guesses = 0
elo_log_loss_sum = 0
rank_log_loss_sum = 0
surface_elo_log_loss_sum = 0

def update_elo_history(elo, name, date, surface, surface_elo):
    elo_history.append(elo)
    elo_players_history.append(name)
    elo_dates_history.append(date)
    surface_history.append(surface)
    surface_elo_history.append(surface_elo)

for index, match in df_matches.iterrows():
    # get players
    nameA = match["winner_name"]
    nameB = match["loser_name"]

    rankA = match["winner_rank"]
    rankB = match["loser_rank"]

    date = match["tourney_date"]

    surface = match["surface"]

    # get current rating of A
    if nameA in players_elo["Overall"]:
        eloA = players_elo["Overall"][nameA]
        if nameA in players_elo[surface]:
            surface_eloA = players_elo[surface][nameA]
        else:
            # haven't played on this surface yet
            surface_eloA = players_elo["Overall"][nameA]
            update_elo_history(eloA, nameA, date, surface, surface_eloA)
    else:
        eloA = 1500 # default value
        surface_eloA = 1500
        update_elo_history(eloA, nameA, date, surface, surface_eloA)

    # get current rating of B
    if nameB in players_elo["Overall"]:
        eloB = players_elo["Overall"][nameB]
        if nameB in players_elo[surface]:
            surface_eloB = players_elo[surface][nameB]
        else:
            # haven't played on this surface yet
            surface_eloB = players_elo["Overall"][nameB]
            update_elo_history(eloB, nameB, date, surface, surface_eloB)
    else:
        eloB = 1500
        surface_eloB = 1500
        update_elo_history(eloB, nameB, date, surface, surface_eloB)

    # Calculate P(A wins)
    pA = get_expected_win_probability(eloA, eloB)

    surface_pA = get_expected_win_probability(surface_eloA, surface_eloB)

    # Find who wins
    S = 1 # A always wins

    # run the model in 2026 to see if the elo system can predict the winning player
    if date >= pd.Timestamp("2026-01-01") and surface == "Grass":
        elo_log_loss_sum += log_loss(S, pA)
        surface_elo_log_loss_sum += log_loss(S, surface_pA)
        rank_log_loss_sum += log_loss(S, win_probability_from_ranking(rankA, rankB))
        if pA > 0.5:
            # elo model guessed correctly
            correct_guesses += 1
        elif pA < 0.5:
            wrong_guesses += 1
        else:
            random_guesses += 1
            guess = random.random()
            if guess >= 0.5:
                # randomly chose correctly
                correct_guesses += 1
            else:
                wrong_guesses += 1

        if surface_pA > 0.5:
            # elo model guessed correctly
            surface_correct_guesses += 1
        elif surface_pA < 0.5:
            surface_wrong_guesses += 1
        else:
            random_guesses += 1
            guess = random.random()
            if guess >= 0.5:
                # randomly chose correctly
                surface_correct_guesses += 1
            else:
                surface_wrong_guesses += 1

    # Update ratings
    eloA, eloB = update_players_elo(eloA, eloB, S)
    surface_eloA, surface_eloB = update_players_elo(surface_eloA, surface_eloB, S)
    players_elo["Overall"][nameA] = eloA
    players_elo["Overall"][nameB] = eloB
    players_elo[surface][nameA] = surface_eloA
    players_elo[surface][nameB] = surface_eloB

    # Update history lists
    update_elo_history(eloA, nameA, date, surface, surface_eloA)
    update_elo_history(eloB, nameB, date, surface, surface_eloB)

df_elos = pd.Series(players_elo["Overall"], name="elo")
df_elos.index.name = "player_name"
df_elos = df_elos.reset_index()
df_elos = df_elos.sort_values("elo", ascending=False)
#print(df_elos)

print(f"Percentage of correct guesses: {(correct_guesses / (correct_guesses+wrong_guesses)) * 100}%")
#print(f"Number of random guesses: {random_guesses}")
print(f"Percentage of surface elo correct guesses: {(surface_correct_guesses / (surface_correct_guesses+surface_wrong_guesses)) * 100}%")

matches_2026 = df_matches[df_matches["tourney_date"] >= pd.Timestamp("2026-01-01")]
#print(len(matches_2026))
print(f"Percentage of highest rank wins 2026: {find_higher_rank_win_percentage(matches_2026)}%")

df_elos_history = pd.DataFrame(
    {
        "date": elo_dates_history,
        "player_name": elo_players_history,
        "elo": elo_history,
        "surface": surface_history,
        "surface_elo": surface_elo_history
    }
)

df_elos_history["date"] = pd.to_datetime(df_elos_history["date"], format="%Y%m%d")


sinner_surface_elo_history = df_elos_history[(df_elos_history["player_name"] == "Jannik Sinner") & (df_elos_history["surface"] == "Grass")]
sinner_elo_history = df_elos_history[df_elos_history["player_name"] == "Jannik Sinner"]

sinner_ranking_history = df_rankings[df_rankings["player"] == "Jannik Sinner"]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,6))
ax1.plot(sinner_surface_elo_history["date"], sinner_surface_elo_history["surface_elo"])
ax2.plot(sinner_ranking_history["ranking_date"], sinner_ranking_history["ranking_points"])
ax1.set_title("Sinner Grass elo over time")
ax1.set_xlabel("Date")
ax1.set_ylabel("Elo")
ax2.set_title("Sinner ranking points over time")
ax2.set_xlabel("Date")
ax2.set_ylabel("Points")
plt.tight_layout()
# plt.savefig("sinner_grass_elo_ranking_graph.png", bbox_inches="tight")
# plt.show()

# Zverev vs Shelton
zverev_elo = df_elos[df_elos["player_name"] == "Alexander Zverev"].iloc[0]["elo"]
shelton_elo = df_elos[df_elos["player_name"] == "Ben Shelton"].iloc[0]["elo"]
#print(get_expected_win_probability(zverev_elo, shelton_elo))
#print(win_probability_from_ranking(2, 9))

# Calculate log loss and compare ranked vs elo methods
average_elo_log_loss = elo_log_loss_sum / (correct_guesses + wrong_guesses)
print(f"Average elo log loss: {average_elo_log_loss}")
average_surface_elo_log_loss = surface_elo_log_loss_sum / (surface_correct_guesses + surface_wrong_guesses)
print(f"Average surface elo log loss: {average_surface_elo_log_loss}")
average_rank_log_loss = rank_log_loss_sum / (correct_guesses + wrong_guesses) # involves data leakage but whatever
print(f"Average rank log loss: {average_rank_log_loss}")
# 0.693 is the baseline for guessing 50/50 each match

# Build separate hard / clay / grass Elo ratings
df_hard_elos = pd.Series(players_elo["Hard"], name="hard_elo")
df_hard_elos.index.name = "player_name"
df_hard_elos = df_hard_elos.reset_index()
df_hard_elos = df_hard_elos.sort_values("hard_elo", ascending=False)
#print(df_hard_elos)

df_clay_elos = pd.Series(players_elo["Clay"], name="clay_elo")
df_clay_elos.index.name = "player_name"
df_clay_elos = df_clay_elos.reset_index()
df_clay_elos = df_clay_elos.sort_values("clay_elo", ascending=False)
#print(df_clay_elos)

df_grass_elos = pd.Series(players_elo["Grass"], name="grass_elo")
df_grass_elos.index.name = "player_name"
df_grass_elos = df_grass_elos.reset_index()
df_grass_elos = df_grass_elos.sort_values("grass_elo", ascending=False)
#print(df_grass_elos)

# Turn each historical match into a row of pre-match features
def upcoming_match_prediction(name1, name2, date, surface):
    head_to_head_info = find_upcoming_match_info(df_matches, name1, name2, date, surface)
    print(head_to_head_info)
    rank1 = head_to_head_info["ranking1"]
    rank2 = head_to_head_info["ranking2"]

    elo_data1 = df_elos_history[(df_elos_history["date"] < date) & (df_elos_history["player_name"] == name1)].iloc[-1]
    elo1 = elo_data1["elo"]
    surface_elo1 = elo_data1["surface_elo"]

    elo_data2 = df_elos_history[(df_elos_history["date"] < date) & (df_elos_history["player_name"] == name2)].iloc[-1]
    elo2 = elo_data2["elo"]
    surface_elo2 = elo_data2["surface_elo"]

    expected_elo_probability = get_expected_win_probability(elo1, elo2)
    expected_surface_elo_probability = get_expected_win_probability(surface_elo1, surface_elo2)
    expected_rank_probability = win_probability_from_ranking(rank1, rank2)

    print(f"Expected win probability elo: {expected_elo_probability}")
    print(f"Expected win probability surface elo: {expected_surface_elo_probability}")
    print(f"Expected win probability rank: {expected_rank_probability}")

upcoming_match_prediction("Alexander Zverev", "Ben Shelton", pd.Timestamp("2026-09-13"), "Hard")

# Build a very simple prediction baseline
