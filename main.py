import numpy
import pandas as pd
import matplotlib.pyplot as plt
import random

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
df_rankings = df_rankings.sort_values("ranking_date", ascending=True)

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

    if total_count == 0:
        return 0
    else:
        return (winner_count / total_count) * 100

print(f"Percentage of higher ranked winner: {find_higher_rank_win_percentage(df_matches)}%")

# Does that percentage differ between hard/clay/grass
print(f"Percentage of higher ranked winner hard: {find_higher_rank_win_percentage(hard_matches)}%")
print(f"Percentage of higher ranked winner clay: {find_higher_rank_win_percentage(clay_matches)}%")
print(f"Percentage of higher ranked winner grass: {find_higher_rank_win_percentage(grass_matches)}%")

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
    rank_diff = rank1 - rank2
    abs_rank_diff = abs(rank_diff)

    for index, x in enumerate(bins):
        print(index)
        if x == 0:
            continue
        if abs_rank_diff <= x:
            probability = df.iloc[index]
            break
        elif abs_rank_diff > 500:
            probability = df.iloc[6]

    if rank_diff > 0: # positive means rank1 is higher than 2
        probability = 1-probability

    return probability

# plt.bar(mid, df, width=widths, color=colors)
# plt.ylim(0, 1)
# plt.xlabel("Rank difference")
# plt.ylabel("Probability of highest rank winning")
# plt.show()

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
#print(f"Current {name} Ranking: {current_ranking}")

date = pd.Timestamp("2025-06-26")

# Build a function that takes two players + a date and returns all of the above

def get_player_stats(df_matches, name, date, surface):
    info_dict = {}

    id = name_to_player(name).iloc[0]["player_id"]
    info_dict["player_id"] = id

    # Find a player's ranking at a given date
    rankings = find_player_rankings(id).sort_values("ranking_date", ascending=False)
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

    id1 = int(player1_info.iloc[0]["player_id"])
    id2 = int(player2_info.iloc[0]["player_id"])

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


# Predict who wins between two players based on who has a higher rank at the time

info = find_upcoming_match_info(df_matches, "Taylor Fritz", "Novak Djokovic", date, "Grass")
print(info)
if info["ranking1"] < info["ranking2"]:
    print("Player 1 wins")
else:
    print("Player 2 wins")

# Build your first Elo rating system

eloA = 1800
eloB = 1200

def get_expected_win_probability(elo1, elo2):
    return 1 / (1 + 10**((elo2-elo1)/400))

def update_elo(elo, win, probability):
    K = 32
    return elo + K * (win - probability)

def update_players_elo(elo1, elo2, win):
    probability = get_expected_win_probability(elo1, elo2)
    return update_elo(elo1, win, probability), update_elo(elo2, 1-win, 1-probability)

df_matches = df_matches.sort_values(["tourney_date", "match_num"], ascending=[True, True]) # sort so first match in list is first dated match
players_elo = {}
elo_dates_history = []
elo_players_history = []
elo_history = []
correct_guesses = 0
wrong_guesses = 0
random_guesses = 0
for index, match in df_matches.iterrows():
    # get players
    nameA = match["winner_name"]
    nameB = match["loser_name"]

    date = match["tourney_date"]

    # get current rating of A
    if nameA in players_elo:
        eloA = players_elo[nameA]
    else:
        eloA = 1500 # default value
        elo_history.append(1500)
        elo_players_history.append(nameA)
        elo_dates_history.append(date)

    # get current rating of B
    if nameB in players_elo:
        eloB = players_elo[nameB]
    else:
        eloB = 1500
        elo_history.append(1500)
        elo_players_history.append(nameB)
        elo_dates_history.append(date)

    # Calculate P(A wins)
    pA = get_expected_win_probability(eloA, eloB)
    pB = get_expected_win_probability(eloB, eloA)

    # Find who wins
    S = 1 # A always wins

    # run the model in 2026 to see if the elo system can predict the winning player
    if date > pd.Timestamp("2026-01-01"):
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

    # Update ratings
    eloA, eloB = update_players_elo(eloA, eloB, S)
    players_elo[nameA] = eloA
    players_elo[nameB] = eloB

    # Update history lists
    elo_history.append(eloA)
    elo_players_history.append(nameA)
    elo_dates_history.append(date)

    elo_history.append(eloB)
    elo_players_history.append(nameB)
    elo_dates_history.append(date)

df_elos = pd.Series(players_elo, name="elo")
df_elos.index.name = "player_name"
df_elos = df_elos.reset_index()
df_elos = df_elos.sort_values("elo", ascending=False)
print(df_elos)

print(f"Percentage of correct guesses: {(correct_guesses / (correct_guesses+wrong_guesses)) * 100}%")
print(f"Number of random guesses: {random_guesses}")

matches_2026 = df_matches[df_matches["tourney_date"] > pd.Timestamp("2026-01-01")]
print(len(matches_2026))
print(f"Percentage of highest rank wins 2026: {find_higher_rank_win_percentage(matches_2026)}%")

df_elos_history = pd.DataFrame(
    {
        "date": elo_dates_history,
        "player_name": elo_players_history,
        "elo": elo_history
    }
)

sinner_elo_history = df_elos_history[df_elos_history["player_name"] == "Jannik Sinner"]

sinner_ranking_history = df_rankings[df_rankings["player"] == 206173]

fig, (ax1, ax2) = plt.subplots(1, 2)

ax1.plot(sinner_elo_history["date"], sinner_elo_history["elo"])
ax2.plot(sinner_ranking_history["ranking_date"], sinner_ranking_history["points"])
ax1.set_title("Sinner elo over time")
ax1.set_xlabel("Date")
ax1.set_ylabel("Elo")
ax2.set_title("Sinner ranking points over time")
ax2.set_xlabel("Date")
ax2.set_ylabel("Points")
plt.show()

# Build separate hard / clay / grass Elo ratings

# Turn each historical match into a row of pre-match features

# Build a very simple prediction baseline
