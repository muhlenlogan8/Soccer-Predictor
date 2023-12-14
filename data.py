import pandas as pd
from helper import clean_strings
from predictors import prepare_data_for_model

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
        
        # Scores can be added to simplify the process. This is allowed due to the pk scores being 0 if the match didn"t go to penalties
        if row["home_score"] + home_pk_score > row["away_score"] + away_pk_score:
            return row["home_team"]
        elif row["home_score"] + home_pk_score < row["away_score"] + away_pk_score:
            return row["away_team"]
        else:
            return "Draw"
        
    df["winner"] = df.apply(determine_winner, axis = 1)
    return df


# Split matches into one big dataframe so for each game each team get their own row
def split_matches(df):

    # Initialize lists
    year_list = []
    team_list = []
    home_away_list = []
    home_score_list = []
    game_score_list = []
    opp_score_list = []
    pk_score_list = []
    opponent_list = []
    winner_list = []

    # Helper function to flip the game_score of originally away teams
    def game_score_helper(score):
        
        # Ensure no strange hyphens are in the score
        score.replace("–", "-")

        # Get just game score
        game_score = score.replace("Awarded[a]", "").replace(" (a.e.t./g.g.)", "").replace(" (a.e.t.)", "")

        # Flip game score
        game_score = game_score[::-1]

        # Add back in extra information
        modified_score = game_score + score[3:]
        return modified_score

    # Go through each match and get the data
    for index, row in df.iterrows():
        # For home team
        year_list.append(row["year"])
        team_list.append(row["home_team"])
        home_away_list.append("Home")
        home_score_list.append(row["home_score"])
        game_score_list.append(row["game_score"])
        opp_score_list.append(row["away_score"])
        pk_score_list.append(row["pk_score"])
        opponent_list.append(row["away_team"])
        winner_list.append(row["winner"])

        # For away team
        year_list.append(row["year"])
        team_list.append(row["away_team"])
        home_away_list.append("Away")
        home_score_list.append(row["away_score"])
        game_score = game_score_helper(row["game_score"])
        game_score_list.append(game_score)
        opp_score_list.append(row["home_score"])
        pk_score_list.append(row["pk_score"])
        opponent_list.append(row["home_team"])
        winner_list.append(row["winner"])

    dict_columns = {"year": year_list, "team": team_list, "home_away": home_away_list, "home_score": home_score_list, "game_score": game_score_list, "opp_score": opp_score_list, "pk_score": pk_score_list, "opponent": opponent_list, "winner": winner_list}
    df_combined = pd.DataFrame(dict_columns)
    return df_combined


# Add rankings to dataframe
def add_rankings(df_matches, df_ranks):

    # Merge the two dataframes on the team column
    df_merged = pd.merge(df_matches, df_ranks[["team", "rank"]], on = "team", how = "left")

    # Rename the rank column
    df_merged.rename(columns={"rank": "team_rank"}, inplace = True)
    
    # Rename team to opponent in df_ranks
    df_ranks.rename(columns = {"team": "opponent"}, inplace = True)
    
    # Merge the two dataframes on the opponent column
    df_merged = pd.merge(df_merged, df_ranks[["opponent", "rank"]], on = "opponent", how = "left")
    
    # # Rename the rank column
    df_merged.rename(columns={"rank": "opp_rank"}, inplace = True)

    # Fill NaN values and convert the team_rank column to integers
    df_merged["team_rank"] = df_merged["team_rank"].fillna(0).astype(int)

    # Restructure columns
    df_result = df_merged[["year", "team", "team_rank", "home_away", "home_score", "game_score", "opp_score", "pk_score", "opponent", "opp_rank", "winner"]]
    return df_result


# Sort df by year column
def sort_by_year(df):
        
        # Sort by year
        df = df.sort_values(by = "year")
        return df


def get_data():
    
    df_matches, df_ranks = pull_json_data()
    df_matches, df_ranks = clean_strings(df_matches, df_ranks)
    df_matches = add_winner(df_matches)
    df_matches = df_matches.reset_index(drop = True)
    df_matches = split_matches(df_matches)
    df_final = add_rankings(df_matches, df_ranks)
    df_final = sort_by_year(df_final)
    return df_final


def prepare_data(df):
    
    df = prepare_data_for_model(df)
    return df


df_test = get_data()
df_test = prepare_data(df_test)