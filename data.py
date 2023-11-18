import pandas as pd

# Read the json file into a dataframe
df_football = pd.read_json("data.json", orient = "split")

# Create a copy of the dataframe
df_mod = df_football.copy()

# Remove the extra information from the game_score column of a provided row. Extra information being " (a.e.t.)" and "–"
def remove_extras(row):
    row["game_score"] = row["game_score"].replace(" (a.e.t.)", "")
    row["game_score"] = row["game_score"].replace("–", "-")
    return row["game_score"]

# Determine the winner of each match and add the winner to the dataframe. Also account for matches that went to penalties, and draws
def determine_winner(row):
    home_score, away_score = map(int, row["game_score"].split("-"))
    if row["pk_score"] != "N/A":
        home_pk_score, away_pk_score = map(int, row["pk_score"].split("-"))
    else:
        home_pk_score, away_pk_score = 0, 0
    
    # Scores can be added to simplify the process. This is allowed due to the pk scores being 0 if the match didn't go to penalties
    if home_score + home_pk_score > away_score + away_pk_score:
        return row["home_team"]
    elif home_score + home_pk_score < away_score + away_pk_score:
        return row["away_team"]
    else:
        return "Draw"

# Apply the remove_extras function to the game_score column of the dataframe that was copied
df_mod["game_score"] = df_mod.apply(remove_extras, axis = 1)

# Apply the determine_winner function to the dataframe that was copied and set this as the original dataframe
df_football["winner"] = df_mod.apply(determine_winner, axis = 1)

print(df_football)