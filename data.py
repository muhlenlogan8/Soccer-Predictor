import pandas as pd
from helper import clean_strings

# pull json data and return two dataframes
def pull_json_data():
    df_matches = pd.read_json("match_data.json", orient = "split")
    df_ranks = pd.read_json("rank_data.json", orient = "split")
    return df_matches, df_ranks


# add winner column to dataframe
def add_winner(df):

    # Determine the winner of each match and add the winner to the dataframe. Also account for matches that went to penalties, and draws
    def determine_winner(row):
        if row["pk_score"] != "N/A":
            home_pk_score, away_pk_score = map(int, row["pk_score"].split("-"))
        else:
            home_pk_score, away_pk_score = 0, 0
        
        # Scores can be added to simplify the process. This is allowed due to the pk scores being 0 if the match didn't go to penalties
        if row["home_score"] + home_pk_score > row["away_score"] + away_pk_score:
            return row["home_team"]
        elif row["home_score"] + home_pk_score < row["away_score"] + away_pk_score:
            return row["away_team"]
        else:
            return "Draw"
        
    df["winner"] = df.apply(determine_winner, axis = 1)
    return df


# NOT WORKING CURRENTLY
def split_matches(df):
    home_cols = {"home_team": "Team", "away_team": "Opponent"}
    home_df = df[["year", "home_team", "home_score", "game_score", "away_score", "pk_score", "away_team", "winner"]].rename(home_cols)
    
    away_cols = {"away_team": "Team", "home_team": "Opponent"}
    away_df = df[["year", "away_team", "away_score", "game_score", "home_score", "pk_score", "home_team", "winner"]].rename(away_cols)
    
    combined_df = pd.concat([home_df, away_df], ignore_index = True)
    return combined_df


def get_data():
    df_matches, df_ranks = pull_json_data()
    df_matches = clean_strings(df_matches)
    df_matches = add_winner(df_matches)
    df_matches = df_matches.reset_index(drop = True)
    print(df_matches)
    


get_data()