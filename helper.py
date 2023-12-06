# data.py helper functions

def combine_like_countries(df):
    
    # Combine same countries for home_team helper function (East Germany and West Germany => Germany, Soviet Union => Russia, FR Yugoslavia => Yugoslavia)
    def combine_home(row):
        if row["home_team"] == "East Germany":
            return "Germany"
        elif row["home_team"] == "West Germany":
            return "Germany"
        elif row["home_team"] == "Soviet Union":
            return "Russia"
        elif row["home_team"] == "FR Yugoslavia":
            return "Yugoslavia"
        return row["home_team"]

    # Combine same contries for away_team helper function
    def combine_away(row):
        if row["away_team"] == "East Germany":
            return "Germany"
        elif row["away_team"] == "West Germany":
            return "Germany"
        elif row["away_team"] == "Soviet Union":
            return "Russia"
        elif row["away_team"] == "FR Yugoslavia":
            return "Yugoslavia"
        return row["away_team"]

    # Apply the respective combine function to the home_team and away_team columns of the dataframe
    df["home_team"] = df.apply(combine_home, axis = 1)
    df["away_team"] = df.apply(combine_away, axis = 1)
    return df


# Stripping of the home_team and away_team columns to remove \xa0 and whitespace
def strip_extras(df):
    
    # Strip the home_team helper function
    def strip_home(row):
        return row["home_team"].strip("\xa0").strip()
    
    # Strip the away_team helper function
    def strip_away(row):
        return row["away_team"].strip("\xa0").strip()
    
    # Apply the respective combine function to the home_team and away_team columns of the dataframe
    df["home_team"] = df.apply(strip_home, axis = 1)
    df["away_team"] = df.apply(strip_away, axis = 1)
    return df 


# BELOW FUNCTION IS NOT NEEDED CURRENTLY
# # Remove the extra information from the game_score column of a provided row. Extra information being " (a.e.t.)" and "–"
# def remove_extras(df):
    
#     # Remove the extra information helper function
#     def remove_extras_helper(row):
#         row["game_score"] = row["game_score"].replace(" (a.e.t./g.g.)", "").replace(" (a.e.t.)", "").replace("–", "-")
    
#     # Apply the remove_extras_helper function to the game_score column of the dataframe
#     print(df["game_score"].unique())
#     df["game_score"] = df.apply(remove_extras_helper, axis = 1)
#     return df


# Clean strings in dataframe
def clean_strings(df):
    df = combine_like_countries(df)
    print("Combined like countries")
    df = strip_extras(df)
    print("Stripped extras")
    return df