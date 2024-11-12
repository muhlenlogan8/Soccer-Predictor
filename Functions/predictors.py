# Functions to set up data for machine learning
import pandas as pd

# Add integer column for winner called "won"
def add_int_winner(df):
    # Add integer column for winner (1 if the team won, 0 if the team lost or drew)
    df['won'] = df.apply(lambda row: 1 if row['team'] == row['winner'] else 0, axis=1)
    return df


# Converts home_away column to integer value, 1 for home team, 0 for away team
def home_away_to_int(df):
    # Convert home_away column to categories then to categories codes (int)
    df["home_away"] = df["home_away"].astype("category").cat.codes
    return df


# Drop unnecessary columns
def drop_columns(df):
    # Drop unnecessary columns
    df = df.drop(columns = ["game_score", "pk_score", "winner"], axis = 1)
    return df


# One-hot encode team and opponent columns
def one_hot_encode(df):
    # One-hot encode team and opponent columns
    team_encoded = pd.get_dummies(df["team"], prefix = "team")
    opponent_encoded = pd.get_dummies(df["opponent"], prefix = "opponent")
    
    # Add columns to df
    df = pd.concat([df, team_encoded, opponent_encoded], axis = 1)
    
    # Mapping of team names to team codes
    team_mapping = pd.Series(team_encoded.columns, index = team_encoded.idxmax(axis = 1).astype(str).values).to_dict()

    # Mapping of opponent names to opponent codes
    opponent_mapping = pd.Series(opponent_encoded.columns, index = opponent_encoded.idxmax(axis = 1).astype(str).values).to_dict()
    
    # Ref dataframes
    team_ref = pd.DataFrame(list(team_mapping.items()), columns = ["team_code", "team"])
    opponent_ref = pd.DataFrame(list(opponent_mapping.items()), columns = ["opponent_code", "opponent"])
    
    # Concatinate ref dataframes
    ref = pd.concat([team_ref, opponent_ref], axis = 1)
    
    # Drop original team and opponent of df
    df = df.drop(columns = ["team", "opponent"], axis = 1)
    return df, ref


# The below fucntion will create a dataframe or dictionary of all possible teams and their encoded values
# This will be used to encode the team and opponent names in df and then return df along with the reference dataframe or dictionary
# The reference dataframe or dictionary will be used to decode the encoded values back to the team and opponent names
def encode_names(df):
    # Create dataframe
    encoded_df = pd.DataFrame()
    
    # Create team column in dataframe and set column elements to every unique value of teams.
    encoded_df["team"] = df["team"].unique()
    encoded_df["team_code"] = range(1, encoded_df.count())
    return df, encoded_df


def prepare_data_for_model(df):
    df = add_int_winner(df)
    # df = home_away_to_int(df)
    df = drop_columns(df)
    return df