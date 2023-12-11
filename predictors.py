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
    df = pd.get_dummies(df, columns = ["team", "opponent"])
    return df


def prepare_data_for_model(df):
    
    df = add_int_winner(df)
    df = home_away_to_int(df)
    df = drop_columns(df)
    return df