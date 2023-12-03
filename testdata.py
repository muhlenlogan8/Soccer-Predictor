import pandas as pd

# Read the json file into a dataframe
df_football = pd.read_json("data.json", orient = "split")

# Initial stripping of the home_team and away_team columns to remove \xa0 and whitespace
df_football["home_team"] = df_football["home_team"].str.strip("\xa0").str.strip()
df_football["away_team"] = df_football["away_team"].str.strip("\xa0").str.strip()

# Combine same countries for home_team (East Germany and West Germany => Germany, Soviet Union => Russia, FR Yugoslavia => Yugoslavia)
def combine_like_countries_home(row):
    if row["home_team"] == "East Germany":
        return "Germany"
    elif row["home_team"] == "West Germany":
        return "Germany"
    elif row["home_team"] == "Soviet Union":
        return "Russia"
    elif row["home_team"] == "FR Yugoslavia":
        return "Yugoslavia"
    return row["home_team"]

# Combine same contries for away_team
def combine_like_countries_away(row):
    if row["away_team"] == "East Germany":
        return "Germany"
    elif row["away_team"] == "West Germany":
        return "Germany"
    elif row["away_team"] == "Soviet Union":
        return "Russia"
    elif row["away_team"] == "FR Yugoslavia":
        return "Yugoslavia"
    return row["away_team"]

# Apply the combine_like_countries function to the home_team and away_team columns of the dataframe
df_football["home_team"] = df_football.apply(combine_like_countries_home, axis = 1)
df_football["away_team"] = df_football.apply(combine_like_countries_away, axis = 1)

# Create a copy of the dataframe
df_mod = df_football.copy()

# Remove the extra information from the game_score column of a provided row. Extra information being " (a.e.t.)" and "–"
def remove_extras(row):
    row["game_score"] = row["game_score"].replace(" (a.e.t./g.g.)", "").replace(" (a.e.t.)", "").replace("–", "-")
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

def add_rank_data(initial_df, rank_df):
    pass

def clean_data():
    pass