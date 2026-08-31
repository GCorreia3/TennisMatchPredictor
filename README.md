# About This Project

As a tennis player myself, this project is an opportunity to learn data analytics and machine learning by predicting the likelihood of a tennis player winning a match.
I will be using real world data of Men's atp matches dating from 2020 up to present.

![alt text](https://github.com/GCorreia3/TennisMatchPredictor/blob/main/prob_rank_winning_vs_rank_dif.png?raw=true)

Cleaned and analysed data to find information from a massive set of matches.
The above image displays how the probability of the higher ranked player winning varies with ranking difference compared to their opponent.
As we can see, the probability starts around 55% and reaches around 75% for the most extreme cases.
This is not surface specific.

![alt text](https://github.com/GCorreia3/Gravity-Simulation/blob/main/sinner_elo_ranking_graph.png?raw=true)

The elo model starts each player at a rating of 1500, and updates each player based on who wins in a match.
If the winner beats someone with a higher elo they will have a large increase in elo and the losing opponent with have a large decrease.
If the winner beats someone with a lower elo, then it is to be expected and thus the elo change is much less.
From this I graphed above the elo change of Jannik Sinner from 2020 to present and compared to how is ranking changes over time.

When predicting the likelihood of a player winning a match, the elo model just outperforms the ranking prediction model by 1% (63.8% to 64.8%).

## Goals:

Completed: Sort and clean data

Completed: Understand and analyse basic information (which players have highest win percentage etc)

Completed: Make a basic model which predicts which player wins based on who has a higher rank

Completed: Create an elo system and run through previous matches to create an elo for each player

In Progress: Improve the elo model and add surface and player dependence

Implement machine learning algorithms to predict the probability of a player winning for a certain match against any opponent


Data from Jeff Sackmann:
https://github.com/Kadantte/tennis_atp
