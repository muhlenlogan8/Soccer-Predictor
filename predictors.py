# Functions to set up data for machine learning

# Converts winner column to integer value, 1 for home team win, 0 for draw, -1 for away team win (home team loss)
def winner_to_int(df):
    
    # Convert winner column to integers helper function
    def winner_to_int_helper(row):
        if row["winner"] == row["team"]:
            return 1
        elif row["winner"] == "Draw":
            return 0
        else:
            return -1
        
    # Apply the winner_to_int_helper function to the dataframe
    df["winner"] = df.apply(winner_to_int_helper, axis = 1)
    return df


# Converts home_away column to integer value, 1 for home team, 0 for away team
def home_away_to_int(df):
    
    # Convert home_away column to categories then to categories codes (int)
    df["home_away"] = df["home_away"].astype("category").cat.codes
    return df


# 


def prepare_data_for_model(df):
    df = winner_to_int(df)
    df = home_away_to_int(df)
    return df