import pandas as pd

df_football = pd.read_json("data.json", orient = "split")
df_mod = df_football.copy()

def remove_extras(row):
    row["game_score"] = row["game_score"].replace(" (a.e.t.)", "")
    row["game_score"] = row["game_score"].replace("–", "-")
    return row["game_score"]

def determine_winner(row):
    home_score, away_score = map(int, row["game_score"].split("-"))
    if row["pk_score"] != "N/A":
        home_pk_score, away_pk_score = map(int, row["pk_score"].split("-"))
    else:
        home_pk_score, away_pk_score = 0, 0
    
    if home_score + home_pk_score > away_score + away_pk_score:
        return row["home_team"]
    elif home_score + home_pk_score < away_score + away_pk_score:
        return row["away_team"]
    else:
        return "Draw"

df_mod["game_score"] = df_mod.apply(remove_extras, axis = 1)
df_football["winner"] = df_mod.apply(determine_winner, axis = 1)

print(df_football)